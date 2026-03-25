import { memo } from 'react';
import { useCartOperations } from '../../hooks/useCart';
import ProductCard from '../ProductCard/ProductCard';
import * as S from './ProductList.styles';

const ProductList = () => {
  const { products, loading, error } = useCartOperations();

  if (loading) {
    return <S.Container>Loading products...</S.Container>;
  }

  if (error) {
    return <S.ErrorMessage>{error}</S.ErrorMessage>;
  }

  if (!products || products.length === 0) {
    return <S.EmptyMessage>No products available</S.EmptyMessage>;
  }

  return (
    <S.Container>
      <S.ProductGrid>
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </S.ProductGrid>
    </S.Container>
  );
};

export default memo(ProductList);
