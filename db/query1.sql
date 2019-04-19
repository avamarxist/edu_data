SELECT Regents.test_id, Demographics.demo_id, Regents.dbn, Regents.year, Regents.exam_name, 
Regents.demo_var AS test_demo, Regents.demo_cat as test_demo_cat, Demographics.demo_var as school_demo, 
Demographics.demo_cat as school_demo_cat, 
Regents.mean_score, Regents.pct_lt_65, Regents.pct_gt_65, Regents.pct_gt_80, 
Demographics.total_enrollment, Regents.test_num, 
Demographics.demo_num as school_demo_num, Demographics.demo_pct AS school_demo_pct 
FROM Regents JOIN Demographics USING (dbn, year) 
WHERE school_demo_cat != 'grade level';