from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.job import Job
from models.user import User
from services.ai_service import AIService
from app import db
from datetime import datetime

bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_jobs():
    """Get all jobs with filtering and pagination"""
    user_id = get_jwt_identity()
    
    # Query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    department = request.args.get('department')
    
    # Build query
    query = Job.query
    
    if status:
        query = query.filter(Job.status == status)
    if department:
        query = query.filter(Job.department == department)
    
    # Pagination
    jobs = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        'jobs': [job.to_dict() for job in jobs.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': jobs.total,
            'pages': jobs.pages,
            'has_next': jobs.has_next,
            'has_prev': jobs.has_prev
        }
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_job():
    """Create a new job posting with AI analysis"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['title', 'description']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create job instance
    job = Job(
        title=data['title'],
        description=data['description'],
        requirements=data.get('requirements'),
        department=data.get('department'),
        location=data.get('location'),
        employment_type=data.get('employment_type', 'full-time'),
        experience_level=data.get('experience_level'),
        salary_min=data.get('salary_min'),
        salary_max=data.get('salary_max'),
        currency=data.get('currency', 'USD'),
        priority=data.get('priority', 'medium'),
        deadline=datetime.fromisoformat(data['deadline']) if data.get('deadline') else None,
        created_by=user_id
    )
    
    try:
        # AI Analysis of Job Description
        ai_service = AIService()
        analysis = ai_service.analyze_job_description(data['description'], data.get('requirements', ''))
        
        job.parsed_skills_list = analysis.get('skills', [])
        job.ai_confidence_score = analysis.get('confidence_score', 0.0)
        job.matching_keywords_list = analysis.get('keywords', [])
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({
            'message': 'Job created successfully',
            'job': job.to_dict(),
            'ai_analysis': analysis
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create job: {str(e)}'}), 500

@bp.route('/<int:job_id>', methods=['GET'])
@jwt_required()
def get_job(job_id):
    """Get a specific job by ID"""
    job = Job.query.get_or_404(job_id)
    
    return jsonify({'job': job.to_dict()}), 200

@bp.route('/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    """Update a job posting"""
    job = Job.query.get_or_404(job_id)
    data = request.get_json()
    
    # Update allowed fields
    allowed_fields = [
        'title', 'description', 'requirements', 'department', 'location',
        'employment_type', 'experience_level', 'salary_min', 'salary_max',
        'currency', 'status', 'priority', 'deadline'
    ]
    
    for field in allowed_fields:
        if field in data:
            if field == 'deadline' and data[field]:
                setattr(job, field, datetime.fromisoformat(data[field]))
            else:
                setattr(job, field, data[field])
    
    try:
        # Re-analyze if description or requirements changed
        if 'description' in data or 'requirements' in data:
            ai_service = AIService()
            analysis = ai_service.analyze_job_description(
                job.description, 
                job.requirements or ''
            )
            
            job.parsed_skills_list = analysis.get('skills', [])
            job.ai_confidence_score = analysis.get('confidence_score', 0.0)
            job.matching_keywords_list = analysis.get('keywords', [])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Job updated successfully',
            'job': job.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update job: {str(e)}'}), 500

@bp.route('/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    """Delete a job posting"""
    job = Job.query.get_or_404(job_id)
    
    try:
        db.session.delete(job)
        db.session.commit()
        
        return jsonify({'message': 'Job deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete job'}), 500

@bp.route('/<int:job_id>/candidates', methods=['GET'])
@jwt_required()
def get_job_candidates(job_id):
    """Get all candidates for a specific job"""
    job = Job.query.get_or_404(job_id)
    
    # Query parameters for filtering
    status = request.args.get('status')
    
    candidates = job.candidates
    if status:
        candidates = [c for c in candidates if c.status == status]
    
    return jsonify({
        'job_id': job_id,
        'job_title': job.title,
        'candidates': [candidate.to_dict() for candidate in candidates],
        'total_candidates': len(candidates)
    }), 200
