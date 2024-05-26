public List<T> findWithOrder(Class<T> entityClass, List<OrderByParameter> orderByParameters) {
    EntityManager entityManager = getEm(); // Ensure EntityManager is injected or created properly
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<T> cq = cb.createQuery(entityClass);
    Root<T> root = cq.from(entityClass);

    cq.distinct(true);

    // Handling multiple order parameters
    List<Order> orders = new ArrayList<>();
    for (OrderByParameter orderByParameter : orderByParameters) {
        Order order = orderByParameter.getOrderBy().equals(OrderByType.ASC) ?
                      cb.asc(root.get(orderByParameter.getName())) :
                      cb.desc(root.get(orderByParameter.getName()));
        orders.add(order);
    }
    if (!orders.isEmpty()) {
        cq.orderBy(orders);
    }

    // Execute the query
    List<T> results = entityManager.createQuery(cq).getResultList();
    return results;
}
