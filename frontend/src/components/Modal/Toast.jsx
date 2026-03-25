import { useEffect } from 'react';
import PropTypes from 'prop-types';
import * as S from './Toast.styles';

const Toast = ({ message, type = 'error', duration = 2000, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const getIcon = () => {
    switch (type) {
      case 'success':
        return '✅';
      case 'warning':
        return '⚠️';
      case 'info':
        return 'ℹ️';
      case 'error':
      default:
        return '❌';
    }
  };

  return (
    <S.ToastContainer>
      <S.ToastContent $type={type}>
        <S.ToastIcon>{getIcon()}</S.ToastIcon>
        <S.ToastMessage>{message}</S.ToastMessage>
      </S.ToastContent>
    </S.ToastContainer>
  );
};

Toast.propTypes = {
  message: PropTypes.string.isRequired,
  type: PropTypes.oneOf(['success', 'warning', 'info', 'error']),
  duration: PropTypes.number,
  onClose: PropTypes.func.isRequired,
};

export default Toast;
