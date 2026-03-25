import api from './api';
import { ENDPOINTS } from '../constants';

/**
 * Cart Service
 * Handles all shopping cart-related API calls
 */

// Fetch cart items
export const getCartItems = async () => {
  const response = await api.get(ENDPOINTS.CART);
  return response.data;
};

// Add item to cart
export const addToCart = async (productId, quantity) => {
  const response = await api.post(ENDPOINTS.CART_ITEMS, {
    product_id: productId,
    quantity,
  });
  return response.data;
};

// Update cart item quantity
export const updateCartItem = async (itemId, quantity) => {
  const response = await api.put(`${ENDPOINTS.CART_ITEMS}/${itemId}`, {
    quantity,
  });
  return response.data;
};

// Remove item from cart
export const removeCartItem = async (itemId) => {
  const response = await api.delete(`${ENDPOINTS.CART_ITEMS}/${itemId}`);
  return response.data;
};

// Clear entire cart (optional feature)
export const clearCart = async () => {
  const response = await api.delete(ENDPOINTS.CART);
  return response.data;
};
