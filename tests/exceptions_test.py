from core.libs.exceptions import FyleError

def test_fyle_error_creation():
    """Test creation of FyleError instances."""
    error_message = "Test error message"
    error_status_code = 400
    
    error = FyleError(error_status_code, error_message)
    
    assert error.status_code == error_status_code
    assert error.message == error_message

def test_fyle_error_to_dict():
    """Test the to_dict method of FyleError."""
    error_message = "Test error message"
    error_status_code = 400
    
    error = FyleError(error_status_code, error_message)
    error_dict = error.to_dict()
    
    assert isinstance(error_dict, dict)
    assert 'message' in error_dict
    assert error_dict['message'] == error_message
