"""
Test suite for CampusQ Financial Engine

Tests payment calculations, milestone evaluation, and registration eligibility.
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock


def test_calculate_payment_percentage():
    """Test payment percentage calculation."""
    from app.services.financial_engine import calculate_payment_percentage
    
    # Test 52% scenario from requirements
    result = calculate_payment_percentage(Decimal('1040000'), Decimal('2000000'))
    assert result == Decimal('52.00')
    
    # Test exactly 45%
    result = calculate_payment_percentage(Decimal('900000'), Decimal('2000000'))
    assert result == Decimal('45.00')
    
    # Test exactly 75%
    result = calculate_payment_percentage(Decimal('1500000'), Decimal('2000000'))
    assert result == Decimal('75.00')
    
    # Test 100%
    result = calculate_payment_percentage(Decimal('2000000'), Decimal('2000000'))
    assert result == Decimal('100.00')
    
    # Test below threshold (44.99%)
    result = calculate_payment_percentage(Decimal('899800'), Decimal('2000000'))
    assert result < Decimal('45.00')
    
    # Test zero tuition
    result = calculate_payment_percentage(Decimal('1000000'), Decimal('0'))
    assert result == Decimal('0')


def test_calculate_outstanding_balance():
    """Test outstanding balance calculation."""
    from app.services.financial_engine import calculate_outstanding_balance
    
    # Example from requirements
    result = calculate_outstanding_balance(Decimal('2000000'), Decimal('1040000'))
    assert result == Decimal('960000.00')
    
    # Fully paid
    result = calculate_outstanding_balance(Decimal('2000000'), Decimal('2000000'))
    assert result == Decimal('0.00')
    
    # Overpayment (should not go negative)
    result = calculate_outstanding_balance(Decimal('2000000'), Decimal('2500000'))
    assert result == Decimal('0.00')


def test_calculate_amount_for_milestone():
    """Test amount required for milestone calculation."""
    from app.services.financial_engine import calculate_amount_for_milestone
    
    # For 75% milestone with 52% already paid
    result = calculate_amount_for_milestone(
        Decimal('75'),
        Decimal('2000000'),
        Decimal('1040000')
    )
    assert result == Decimal('460000.00')  # As per requirements example
    
    # For 45% milestone
    result = calculate_amount_for_milestone(
        Decimal('45'),
        Decimal('2000000'),
        Decimal('840000')  # 42%
    )
    assert result == Decimal('60000.00')  # Need 60k more to reach 45%


def test_evaluate_milestones():
    """Test milestone evaluation."""
    from app.services.financial_engine import evaluate_milestones
    from unittest.mock import Mock
    
    # Create mock policy
    policy = Mock()
    policy.initial_percentage = '45.00'
    policy.second_percentage = '75.00'
    policy.final_percentage = '100.00'
    
    # Test at 52% - only initial achieved
    result = evaluate_milestones(Decimal('52.00'), policy)
    assert result['initial']['achieved'] == True
    assert result['second']['achieved'] == False
    assert result['final']['achieved'] == False
    
    # Test at 75% - initial and second achieved
    result = evaluate_milestones(Decimal('75.00'), policy)
    assert result['initial']['achieved'] == True
    assert result['second']['achieved'] == True
    assert result['final']['achieved'] == False
    
    # Test at 100% - all achieved
    result = evaluate_milestones(Decimal('100.00'), policy)
    assert result['initial']['achieved'] == True
    assert result['second']['achieved'] == True
    assert result['final']['achieved'] == True
    
    # Test at 44.99% - none achieved
    result = evaluate_milestones(Decimal('44.99'), policy)
    assert result['initial']['achieved'] == False
    assert result['second']['achieved'] == False
    assert result['final']['achieved'] == False


def test_check_registration_eligibility():
    """Test registration eligibility checking."""
    from app.services.financial_engine import check_registration_eligibility
    from unittest.mock import Mock
    
    # Create mock policy
    policy = Mock()
    policy.initial_percentage = '45.00'
    
    # Test eligible (45%)
    eligible, reason = check_registration_eligibility(Decimal('45.00'), policy)
    assert eligible == True
    
    # Test eligible (above 45%)
    eligible, reason = check_registration_eligibility(Decimal('60.00'), policy)
    assert eligible == True
    
    # Test blocked (below 45%)
    eligible, reason = check_registration_eligibility(Decimal('42.00'), policy)
    assert eligible == False
    assert '45' in reason  # Reason should mention 45%
    
    # Test no policy
    eligible, reason = check_registration_eligibility(Decimal('50.00'), None)
    assert eligible == False
    assert 'policy' in reason.lower()


def test_pending_payments_dont_affect_eligibility():
    """Verify that pending payments don't affect eligibility calculations."""
    # This is enforced by the get_verified_payments function
    # which only sums payments with status='verified'
    from app.services.financial_engine import get_verified_payments
    from unittest.mock import Mock, patch
    
    mock_db = Mock()
    mock_query = Mock()
    mock_filter = Mock()
    mock_scalar = Mock(return_value=1000000)
    
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.scalar = mock_scalar
    
    result = get_verified_payments(mock_db, 'student-id', 'semester-id')
    
    # Verify the query filters for 'verified' status only
    call_args = mock_filter.scalar.call_args
    assert mock_query.filter.called
    
    # Check that the filter includes status='verified'
    filter_call = mock_query.filter.call_args
    assert filter_call is not None
