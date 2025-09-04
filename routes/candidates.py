from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.candidate import Candidate
from models.job import Job
from services.ai_service import AIService
from services.outreach_service import OutreachService
from app import db
from datetime import datetime

bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_candidates():
    """Get all candidates with filtering and pagination"""
    # Query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    job_id = request.args.get('job_id', type=int)
    
    # Build query
    query = Candidate.query
    
    if status:
        query = query.filter(Candidate.status == status)
    if job_id:
        query = query.filter(Candidate.job_id == job_id)
    
    # Pagination
    candidates = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        'candidates': [candidate.to_dict() for candidate in candidates.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': candidates.total,
            'pages': candidates.pages,
            'has_next': candidates.has_next,
            'has_prev': candidates.has_prev
        }
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_candidate():
    """Create a new candidate with AI analysis"""
    data = request.get_json()
    
    required_fields = ['first_name', 'last_name', 'email', 'job_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Verify job exists
    job = Job.query.get(data['job_id'])
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    # Check if candidate already exists for this job
    existing = Candidate.query.filter_by(
        email=data['email'], 
        job_id=data['job_id']
    ).first()
    if existing:
        return jsonify({'error': 'Candidate already exists for this job'}), 409
    
    # Create candidate
    candidate = Candidate(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
        linkedin_url=data.get('linkedin_url'),
        resume_url=data.get('resume_url'),
        current_title=data.get('current_title'),
        current_company=data.get('current_company'),
        experience_years=data.get('experience_years'),
        location=data.get('location'),
        source=data.get('source', 'manual'),
        preferred_contact_method=data.get('preferred_contact_method', 'email'),
        timezone=data.get('timezone'),
        job_id=data['job_id']
    )
    
    if data.get('skills'):
        candidate.skills_list = data['skills']
    
    try:
        # AI Analysis of candidate against job
        ai_service = AIService()
        if candidate.resume_url or candidate.linkedin_url:
            analysis = ai_service.analyze_candidate_match(candidate, job)
            candidate.ai_confidence_score = analysis.get('confidence_score', 0.0)
            candidate.matching_rationale = analysis.get('rationale', '')
            candidate.parsed_resume_dict = analysis.get('parsed_data', {})
        
        db.session.add(candidate)
        db.session.commit()
        
        return jsonify({
            'message': 'Candidate created successfully',
            'candidate': candidate.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create candidate: {str(e)}'}), 500

@bp.route('/<int:candidate_id>', methods=['GET'])
@jwt_required()
def get_candidate(candidate_id):
    """Get a specific candidate by ID"""
    candidate = Candidate.query.get_or_404(candidate_id)
    
    return jsonify({'candidate': candidate.to_dict()}), 200

@bp.route('/<int:candidate_id>', methods=['PUT'])
@jwt_required()
def update_candidate(candidate_id):
    """Update a candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    data = request.get_json()
    
    # Update allowed fields
    allowed_fields = [
        'first_name', 'last_name', 'phone', 'linkedin_url', 'resume_url',
        'current_title', 'current_company', 'experience_years', 'location',
        'status', 'preferred_contact_method', 'timezone', 'expected_salary_min',
        'expected_salary_max', 'notice_period_days'
    ]
    
    for field in allowed_fields:
        if field in data:
            setattr(candidate, field, data[field])
    
    if 'skills' in data:
        candidate.skills_list = data['skills']
    
    try:
        db.session.commit()
        
        return jsonify({
            'message': 'Candidate updated successfully',
            'candidate': candidate.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update candidate: {str(e)}'}), 500

@bp.route('/bulk-approve', methods=['POST'])
@jwt_required()
def bulk_approve_candidates():
    """Approve multiple candidates for outreach"""
    data = request.get_json()
    
    if not data or 'candidate_ids' not in data:
        return jsonify({'error': 'candidate_ids required'}), 400
    
    candidate_ids = data['candidate_ids']
    candidates = Candidate.query.filter(Candidate.id.in_(candidate_ids)).all()
    
    if len(candidates) != len(candidate_ids):
        return jsonify({'error': 'Some candidates not found'}), 404
    
    try:
        outreach_service = OutreachService()
        results = []
        
        for candidate in candidates:
            if candidate.status == 'sourced':
                candidate.status = 'approved'
                
                # Initiate outreach
                outreach_result = outreach_service.initiate_outreach(candidate)
                results.append({
                    'candidate_id': candidate.id,
                    'status': 'approved',
                    'outreach_initiated': outreach_result
                })
            else:
                results.append({
                    'candidate_id': candidate.id,
                    'status': 'skipped',
                    'reason': f'Current status: {candidate.status}'
                })
        
        db.session.commit()
        
        return jsonify({
            'message': 'Bulk approval completed',
            'results': results
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to approve candidates: {str(e)}'}), 500

@bp.route('/<int:candidate_id>/outreach-history', methods=['GET'])
@jwt_required()
def get_candidate_outreach_history(candidate_id):
    """Get outreach history for a candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    
    outreach_history = [outreach.to_dict() for outreach in candidate.outreach_history]
    
    return jsonify({
        'candidate_id': candidate_id,
        'outreach_history': outreach_history
    }), 200

@bp.route('/<int:candidate_id>/interviews', methods=['GET'])
@jwt_required()
def get_candidate_interviews(candidate_id):
    """Get all interviews for a candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    
    interviews = [interview.to_dict() for interview in candidate.interviews]
    
    return jsonify({
        'candidate_id': candidate_id,
        'interviews': interviews
    }), 200
