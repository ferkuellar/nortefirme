from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

class VoltageType(str, Enum):
    LOW_VOLTAGE = "low_voltage"
    MEDIUM_VOLTAGE = "medium_voltage"
    LOW_AND_MEDIUM_VOLTAGE = "low_and_medium_voltage"
    NOT_APPLICABLE = "not_applicable"

class ProjectStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class AssetType(str, Enum):
    COVER_IMAGE = "cover_image"
    GALLERY_IMAGE = "gallery_image"
    BEFORE_IMAGE = "before_image"
    AFTER_IMAGE = "after_image"
    TECHNICAL_DOCUMENT = "technical_document"
    DELIVERY_EVIDENCE = "delivery_evidence"

class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    QUOTED = "quoted"
    WON = "won"
    LOST = "lost"
    SPAM = "spam"
