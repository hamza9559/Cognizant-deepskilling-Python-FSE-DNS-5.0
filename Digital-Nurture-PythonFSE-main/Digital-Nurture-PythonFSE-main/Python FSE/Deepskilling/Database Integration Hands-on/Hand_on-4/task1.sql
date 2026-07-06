-- ===========================
-- Hands-On 4 : Task 1
-- Baseline Performance (No Indexes)
-- ===========================

-- 48. Run EXPLAIN on the query
EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;
