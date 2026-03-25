import PropTypes from 'prop-types';
import * as S from './Modal.styles';

// Confirmation Modal Component
const ConfirmationModal = ({
  isOpen,
  title,
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  onConfirm,
  onCancel,
  type = 'danger',
}) => {
  if (!isOpen) return null;

  const getButtonColor = () => {
    switch (type) {
      case 'danger':
        return '#d32f2f';
      case 'warning':
        return '#ff9800';
      case 'info':
        return '#1976d2';
      default:
        return '#d32f2f';
    }
  };

  return (
    <S.ConfirmOverlay>
      <S.ConfirmBox>
        <S.ConfirmText>{message}</S.ConfirmText>
        <S.ConfirmButtons>
          <S.CancelButton onClick={onCancel}>{cancelText}</S.CancelButton>
          <S.ConfirmActionButton 
            onClick={onConfirm}
            $buttonColor={getButtonColor()}
          >
            {confirmText}
          </S.ConfirmActionButton>
        </S.ConfirmButtons>
      </S.ConfirmBox>
    </S.ConfirmOverlay>
  );
};

ConfirmationModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  title: PropTypes.string.isRequired,
  message: PropTypes.string.isRequired,
  confirmText: PropTypes.string,
  cancelText: PropTypes.string,
  onConfirm: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
  type: PropTypes.oneOf(['danger', 'warning', 'info']),
};

export default ConfirmationModal;
