/**
 * Validator Functions for input validation
 */

/**
 * Validate quantity input value
 * @param {any} value - Value to validate
 * @param {object} options - Validation options
 * @param {number} options.min - Minimum value (default: 1)
 * @param {number} options.max - Maximum value (default: 99)
 * @param {boolean} options.required - Whether value is required (default: true)
 * @returns {object} Validation result with isValid and message
 */
export const validateQuantityInput = (value, options = {}) => {
  const { min = 1, max = 99, required = true } = options;
  
  if (required && (!value || value === '')) {
    return { isValid: false, message: 'Quantity is required' };
  }
  
  if (value === '' || value == null) {
    return { isValid: true, message: '' }; // Empty but not required
  }
  
  const num = Number(value);
  if (isNaN(num)) {
    return { isValid: false, message: 'Quantity must be a number' };
  }
  
  if (!Number.isInteger(num)) {
    return { isValid: false, message: 'Quantity must be an integer' };
  }
  
  if (num < min) {
    return { isValid: false, message: `Minimum quantity is ${min}` };
  }
  
  if (num > max) {
    return { isValid: false, message: `Maximum quantity is ${max}` };
  }
  
  return { isValid: true, message: '' };
};

/**
 * Parse quantity input value safely
 * @param {string} value - Value to parse
 * @param {object} options - Parse options
 * @param {number} options.min - Minimum allowed value (default: 1)
 * @param {number} options.max - Maximum allowed value (default: 99)
 * @returns {object} Parsed result with parsed value and isValid flag
 */
export const parseQuantityValue = (value, options = {}) => {
  const { min = 1, max = 99 } = options;
  
  // Handle empty string
  if (value === '' || value == null) {
    return { parsed: '', isValid: true };
  }
  
  const parsed = parseInt(value);
  
  if (isNaN(parsed) || parsed < min || parsed > max) {
    return { parsed: value, isValid: false };
  }
  
  return { parsed, isValid: true };
};

/**
 * Check stock status based on quantity
 * @param {number} stockQuantity - Available stock quantity
 * @param {number} threshold - Low stock threshold (default: 5)
 * @returns {object} Stock status object with status, label, and warning flag
 */
export const checkStockStatus = (stockQuantity, threshold = 5) => {
  if (stockQuantity <= 0) {
    return { 
      status: 'out_of_stock', 
      label: 'Out of stock', 
      warning: false,
      icon: '❌'
    };
  }
  
  if (stockQuantity <= threshold) {
    return { 
      status: 'low_stock', 
      label: `${stockQuantity} in stock`, 
      warning: true,
      icon: '⚠️'
    };
  }
  
  return { 
    status: 'in_stock', 
    label: `${stockQuantity} in stock`, 
    warning: false,
    icon: ''
  };
};
