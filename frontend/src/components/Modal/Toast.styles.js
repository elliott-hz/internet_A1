import styled from 'styled-components';

export const ToastContainer = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10000;
  animation: slideInCenter 0.3s ease;

  @keyframes slideInCenter {
    from {
      transform: translate(-50%, -60%);
      opacity: 0;
    }
    to {
      transform: translate(-50%, -50%);
      opacity: 1;
    }
  }
`;

export const ToastContent = styled.div`
  background-color: ${(props) => {
    switch (props.$type) {
      case 'success':
        return '#4caf50';
      case 'warning':
        return '#ff9800';
      case 'info':
        return '#2196f3';
      case 'error':
      default:
        return '#dc3545';
    }
  }};
  color: white;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 280px;
  max-width: 400px;
  font-size: 15px;
  line-height: 1.4;
`;

export const ToastIcon = styled.span`
  font-size: 20px;
  flex-shrink: 0;
`;

export const ToastMessage = styled.span`
  flex: 1;
  word-break: break-word;
`;
