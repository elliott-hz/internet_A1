import styled from 'styled-components';

export const ItemContainer = styled.div`
  padding: 16px 0;
  border-bottom: 1px solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }
`;

export const ItemInfo = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
`;

export const ItemName = styled.h4`
  font-size: 16px;
  color: #333;
  margin: 0;
  font-weight: 500;
`;

export const ItemTotal = styled.span`
  font-size: 18px;
  color: #2e7d32;
  font-weight: 600;
`;

export const ItemDetails = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
`;

export const UnitPrice = styled.span`
  font-size: 13px;
  color: #666;
  font-weight: 500;
`;

export const Controls = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex: 1;
`;

export const QuantityControl = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
`;

export const QuantityButton = styled.button`
  width: 32px;
  height: 32px;
  border: none;
  background-color: #f5f5f5;
  color: #333;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s ease;

  &:hover:not(:disabled) {
    background-color: #e0e0e0;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

export const QuantityDisplay = styled.span`
  min-width: 32px;
  text-align: center;
  font-size: 16px;
  font-weight: 500;
  color: #333;
`;

export const RemoveButton = styled.button`
  padding: 8px 16px;
  background-color: transparent;
  color: #d32f2f;
  border: 1px solid #d32f2f;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover:not(:disabled) {
    background-color: #d32f2f;
    color: white;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

