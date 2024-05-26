  criteriaQuery.where(cb.and(predicates.toArray(new Predicate[0])));
    if (lazyData.getPageSize() != SearchData.UNBOUNDED_RESULTSET) {
        TypedQuery<T> query = entityManager.createQuery(criteriaQuery);
        query.setFirstResult(lazyData.getStart());
        query.setMaxResults(lazyData.getPageSize());
        List<T> results = query.getResultList();

        // Query for counting total results
        CriteriaQuery<Long> countQuery = cb.createQuery(Long.class);
        Root<T> countRoot = countQuery.from(entityClass);
        countQuery.select(cb.count(countRoot));
        countQuery.where(cb.and(predicates.toArray(new Predicate[0])));

        Long count = entityManager.createQuery(countQuery).getSingleResult();
        int total = (count != null) ? count.intValue() : 0;
        lazyData.setCount(total);

        return results;
    } else {
        return entityManager.createQuery(criteriaQuery).getResultList();
    }
