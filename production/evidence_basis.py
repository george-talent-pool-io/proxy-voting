"""A model's complete-input negative is an audit basis, never a quotation.

It can support automation only after calibration/qualification covers this exact
basis. It does not assert that software proved semantic absence in the source.
"""
import hashlib

KIND='MODEL_NEGATIVE_AFTER_COMPLETE_SOURCE_V1'


def negative_basis(text,model_identity):
    return {'kind':KIND,'source_sha256':hashlib.sha256(text.encode()).hexdigest(),
            'model_identity':model_identity,'complete_source_processed':True,
            'meaning':'Model classified NO after the complete source; no supporting quotation identified',
            'requires_basis_specific_calibration':True}


def valid_negative_basis(text,pred):
    basis=pred.get('negative_basis') or {}
    return bool(pred.get('value')=='NO' and basis.get('kind')==KIND and basis.get('model_identity') and
                basis.get('complete_source_processed') is True and not pred.get('truncated') and
                basis.get('source_sha256')==hashlib.sha256(text.encode()).hexdigest())
