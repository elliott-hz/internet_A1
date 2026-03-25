import styled from 'styled-components';

export const Container = styled.div`
  width: 100%;
  height: 100%;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: calc(120px + 20px);
  max-height: calc(100vh - (120px + 40px));
`;

export const Title = styled.h2`
  font-size: 24px;
  margin: 0 0 20px 0;
  color: #333;
  border-bottom: 2px solid #f5f5f5;
  padding-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-weight: 700;
`;

export const CartIcon = styled.span`
  font-size: 28px;
`;

export const CartContent = styled.div`
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
`;

export const CartSummary = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
`;

export const ItemCount = styled.span`
  font-size: 14px;
  color: #666;
  font-weight: 500;
`;

export const ClearCartButton = styled.button`
  padding: 6px 12px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 4px;

  &:hover {
    background-color: #d32f2f;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(244, 67, 54, 0.3);
  }

  &:active {
    transform: translateY(0);
  }
`;

export const CartItemsList = styled.div`
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
  min-height: 0;

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: #bdbdbd;
    border-radius: 4px;

    &:hover {
      background: #9e9e9e;
    }
  }
`;

export const TotalSection = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 2px solid #f5f5f5;
  flex-shrink: 0;
`;

export const TotalLabel = styled.span`
  font-size: 18px;
  font-weight: 600;
  color: #333;
`;

export const TotalAmount = styled.span`
  font-size: 24px;
  font-weight: bold;
  color: #2e7d32;
`;

export const EmptyCart = styled.div`
  text-align: center;
  padding: 40px 20px;
  color: #9e9e9e;
  font-size: 16px;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
`;

export const ErrorMessage = styled.div`
  color: #d32f2f;
  padding: 20px;
  text-align: center;
`;

export const StockErrorAlert = styled.div`
  position: relative;
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 6px;
  padding: 12px 40px 12px 16px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  animation: slideDown 0.3s ease-out;

  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

export const ErrorContent = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
`;

export const ErrorIcon = styled.span`
  font-size: 20px;
  flex-shrink: 0;
`;

export const ErrorMessageText = styled.span`
  font-size: 14px;
  color: #856404;
  line-height: 1.5;
  word-break: break-word;
`;

export const CloseButton = styled.button`
  position: absolute;
  top: 8px;
  right: 8px;
  background: transparent;
  border: none;
  font-size: 24px;
  line-height: 1;
  color: #856404;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;

  &:hover {
    background: rgba(133, 100, 4, 0.1);
    transform: rotate(90deg);
  }
`;

