"""
Business Licensing and Sales System for CodeCraft Studio
Production-ready sales capabilities with license protection
© 2025 Ervin Remus Radosavlevici - All Rights Reserved
"""

import json
import os
import logging
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from app import db
from security.rados_security import log_security_event


class BusinessLicense(db.Model):
    """Business license management for CodeCraft Studio"""
    __tablename__ = 'business_licenses'
    
    id = Column(Integer, primary_key=True)
    license_key = Column(String(255), unique=True, nullable=False)
    license_type = Column(String(100), nullable=False)  # personal, commercial, enterprise
    customer_name = Column(String(200), nullable=False)
    customer_email = Column(String(255), nullable=False)
    company_name = Column(String(255))
    purchase_amount = Column(Float, nullable=False)
    
    # License status and validity
    status = Column(String(50), default='active')  # active, suspended, expired, revoked
    valid_from = Column(DateTime, default=datetime.utcnow)
    valid_until = Column(DateTime)
    usage_count = Column(Integer, default=0)
    max_usage = Column(Integer, default=100)  # -1 for unlimited
    
    # Content protection
    watermark_enabled = Column(Boolean, default=True)
    commercial_rights = Column(Boolean, default=False)
    redistribution_rights = Column(Boolean, default=False)
    modification_rights = Column(Boolean, default=False)
    
    # Audit trail
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)
    last_validation = Column(DateTime)
    
    def __repr__(self):
        return f'<BusinessLicense {self.license_key}: {self.license_type}>'
    
    def to_dict(self):
        return {
            'license_key': self.license_key,
            'license_type': self.license_type,
            'customer_name': self.customer_name,
            'status': self.status,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'usage_count': self.usage_count,
            'max_usage': self.max_usage,
            'commercial_rights': self.commercial_rights,
            'created_at': self.created_at.isoformat()
        }


class SalesRecord(db.Model):
    """Sales tracking for business analytics"""
    __tablename__ = 'sales_records'
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String(255), unique=True, nullable=False)
    license_id = Column(Integer, nullable=False)
    
    # Customer information
    customer_name = Column(String(200), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_country = Column(String(100))
    
    # Product details
    product_type = Column(String(100), nullable=False)
    product_name = Column(String(255), nullable=False)
    sale_amount = Column(Float, nullable=False)
    currency = Column(String(10), default='USD')
    
    # Payment information
    payment_method = Column(String(50))
    payment_status = Column(String(50), default='completed')
    payment_date = Column(DateTime, default=datetime.utcnow)
    
    # Metadata
    referral_source = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'customer_name': self.customer_name,
            'product_name': self.product_name,
            'sale_amount': self.sale_amount,
            'currency': self.currency,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }


class BusinessLicenseManager:
    """Manages business licenses and sales operations"""
    
    LICENSE_TYPES = {
        'personal': {
            'name': 'Personal License',
            'price': 49.99,
            'max_usage': 100,
            'commercial_rights': False,
            'validity_days': 365
        },
        'commercial': {
            'name': 'Commercial License', 
            'price': 199.99,
            'max_usage': 500,
            'commercial_rights': True,
            'validity_days': 365
        },
        'enterprise': {
            'name': 'Enterprise License',
            'price': 999.99,
            'max_usage': -1,  # Unlimited
            'commercial_rights': True,
            'validity_days': 365
        }
    }
    
    def __init__(self):
        self.protection_active = True
        log_security_event("LICENSE_MANAGER_INIT", "Business license manager initialized")
    
    def generate_license_key(self, license_type, customer_email):
        """Generate unique license key"""
        import hashlib
        import secrets
        
        timestamp = str(int(datetime.utcnow().timestamp()))
        random_part = secrets.token_hex(8)
        content = f"{license_type}_{customer_email}_{timestamp}_{random_part}"
        
        # Create license key with checksum
        key_hash = hashlib.sha256(content.encode()).hexdigest()[:16].upper()
        license_key = f"CCS-{license_type.upper()[:3]}-{key_hash}-{timestamp[-4:]}"
        
        return license_key
    
    def create_license(self, license_type, customer_name, customer_email, company_name=None):
        """Create new business license"""
        try:
            if license_type not in self.LICENSE_TYPES:
                raise ValueError(f"Invalid license type: {license_type}")
            
            license_info = self.LICENSE_TYPES[license_type]
            license_key = self.generate_license_key(license_type, customer_email)
            
            # Calculate validity period
            valid_until = datetime.utcnow() + timedelta(days=license_info['validity_days'])
            
            # Create license record
            license_record = BusinessLicense(
                license_key=license_key,
                license_type=license_type,
                customer_name=customer_name,
                customer_email=customer_email,
                company_name=company_name,
                purchase_amount=license_info['price'],
                valid_until=valid_until,
                max_usage=license_info['max_usage'],
                commercial_rights=license_info['commercial_rights'],
                redistribution_rights=license_type == 'enterprise',
                modification_rights=license_type in ['commercial', 'enterprise']
            )
            
            db.session.add(license_record)
            db.session.commit()
            
            log_security_event("LICENSE_CREATED", f"License created: {license_key} for {customer_email}")
            return license_record
            
        except Exception as e:
            log_security_event("LICENSE_CREATION_ERROR", str(e), "ERROR")
            raise
    
    def validate_license(self, license_key):
        """Validate license key and update usage"""
        try:
            license_record = BusinessLicense.query.filter_by(license_key=license_key).first()
            
            if not license_record:
                log_security_event("LICENSE_VALIDATION_FAILED", f"License not found: {license_key}", "WARNING")
                return False, "License key not found"
            
            # Check license status
            if license_record.status != 'active':
                log_security_event("LICENSE_VALIDATION_FAILED", f"License inactive: {license_key}", "WARNING")
                return False, f"License is {license_record.status}"
            
            # Check expiration
            if license_record.valid_until and datetime.utcnow() > license_record.valid_until:
                license_record.status = 'expired'
                db.session.commit()
                log_security_event("LICENSE_EXPIRED", f"License expired: {license_key}", "WARNING")
                return False, "License has expired"
            
            # Check usage limits
            if license_record.max_usage != -1 and license_record.usage_count >= license_record.max_usage:
                log_security_event("LICENSE_USAGE_EXCEEDED", f"Usage limit exceeded: {license_key}", "WARNING")
                return False, "Usage limit exceeded"
            
            # Update usage and validation timestamp
            license_record.usage_count += 1
            license_record.last_used = datetime.utcnow()
            license_record.last_validation = datetime.utcnow()
            db.session.commit()
            
            log_security_event("LICENSE_VALIDATED", f"License validated: {license_key}")
            return True, license_record
            
        except Exception as e:
            log_security_event("LICENSE_VALIDATION_ERROR", str(e), "ERROR")
            return False, "Validation error"
    
    def get_license_info(self, license_key):
        """Get license information"""
        license_record = BusinessLicense.query.filter_by(license_key=license_key).first()
        return license_record.to_dict() if license_record else None
    
    def record_sale(self, license_record, payment_details=None):
        """Record a sale transaction"""
        try:
            import secrets
            transaction_id = f"TXN-{secrets.token_hex(8).upper()}"
            
            sale_record = SalesRecord(
                transaction_id=transaction_id,
                license_id=license_record.id,
                customer_name=license_record.customer_name,
                customer_email=license_record.customer_email,
                product_type=license_record.license_type,
                product_name=f"CodeCraft Studio {license_record.license_type.title()} License",
                sale_amount=license_record.purchase_amount,
                payment_method=payment_details.get('method', 'manual') if payment_details else 'manual',
                payment_status='completed'
            )
            
            db.session.add(sale_record)
            db.session.commit()
            
            log_security_event("SALE_RECORDED", f"Sale recorded: {transaction_id}")
            return sale_record
            
        except Exception as e:
            log_security_event("SALE_RECORDING_ERROR", str(e), "ERROR")
            raise
    
    def get_sales_analytics(self):
        """Get sales analytics for business dashboard"""
        try:
            total_sales = db.session.query(SalesRecord).count()
            total_revenue = db.session.query(db.func.sum(SalesRecord.sale_amount)).scalar() or 0
            
            # Sales by license type
            sales_by_type = db.session.query(
                SalesRecord.product_type,
                db.func.count(SalesRecord.id),
                db.func.sum(SalesRecord.sale_amount)
            ).group_by(SalesRecord.product_type).all()
            
            # Active licenses
            active_licenses = BusinessLicense.query.filter_by(status='active').count()
            
            return {
                'total_sales': total_sales,
                'total_revenue': float(total_revenue),
                'active_licenses': active_licenses,
                'sales_by_type': [
                    {
                        'type': row[0],
                        'count': row[1],
                        'revenue': float(row[2])
                    } for row in sales_by_type
                ]
            }
            
        except Exception as e:
            log_security_event("ANALYTICS_ERROR", str(e), "ERROR")
            return {'error': 'Analytics unavailable'}
    
    def apply_content_protection(self, content, license_record):
        """Apply content protection based on license"""
        if not license_record or not license_record.watermark_enabled:
            return content
        
        protection_notice = f"""
        
        🛡️ PROTECTED CONTENT - CodeCraft Studio
        Licensed to: {license_record.customer_name}
        License: {license_record.license_key}
        © 2025 Ervin Remus Radosavlevici - All Rights Reserved
        
        This content is protected under the Radosavlevici Game License v1.0
        Unauthorized use, reproduction, or distribution is prohibited.
        """
        
        return content + protection_notice


# Initialize license manager instance
license_manager = BusinessLicenseManager()