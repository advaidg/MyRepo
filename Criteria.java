@Override
public List<T> findForAutoComplete(Class<T> entityClass, List<String> searchBys, String value, String orderBy, boolean ignoreCase) {
    EntityManager entityManager = ...; // Ensure EntityManager is injected or created properly
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<T> cq = cb.createQuery(entityClass);
    Root<T> root = cq.from(entityClass);
    
    // Handling multiple search conditions with OR
    List<Predicate> predicates = new ArrayList<>();
    if (searchBys != null && !searchBys.isEmpty()) {
        String likedValue = "%" + value.replace("'", "''") + "%"; // SQL injection prevention
        for (String searchBy : searchBys) {
            Predicate condition = ignoreCase ?
                cb.like(cb.lower(root.get(searchBy)), likedValue.toLowerCase()) :
                cb.like(root.get(searchBy), likedValue);
            predicates.add(condition);
        }
        cq.where(cb.or(predicates.toArray(new Predicate[0])));
    }

    // Handling distinct results and ordering
    cq.distinct(true);
    if (orderBy != null && !orderBy.isEmpty()) {
        cq.orderBy(cb.asc(root.get(orderBy)));
    }

    // Execute the query
    List<T> results = entityManager.createQuery(cq).getResultList();
    return results;
}
