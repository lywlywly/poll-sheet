.mode column
SELECT
    A.id,
    A.content,
    D.type,
    D.text,
    D.group_id_id as entry_group_id,
    B.choice_text,
    C.name,
    C.net_id,
    C.group_id_id as student_group_id
FROM
    students_vote A
    JOIN students_choice B on A.choice_id = B.id
    JOIN students_student C on A.voter_id = C.id
    JOIN students_entry D ON B.poll_id = D.id;