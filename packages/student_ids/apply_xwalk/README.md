This bundle expects

* an environment variable / command-line parameter `EARTHMOVER_NODE_TO_XWALK` which currently varies by assessment (`$sources.nwea_map_input`, `$sources.cli_circle_input`, etc.), but could we standardize on `$sources.input_file` or `$sources.input` so we wouldn't need this?
* `$sources.student_id_match_rates` with the following shape:

| source_column_name | edfi_column_name | num_matches | num_rows | match_rate |
| --- | --- | --- | --- | --- |
| StudentID | Local | 4 | 6 | 0.6666666666666666 |
| Student_StateID | Local | 1 | 6 | 0.16666666666666666 |

    which can be added as either
    ```yaml
    source:
      student_id_match_rates:
        file: /efs/path/to/{assessment_id}/{tenant_code}/{school_year}/student_id_match_rates.csv
        header_rows: 1
        # or, from Snowflake:
        connection: "snowflake://$SNOWFLAKE_USER:$SNOWFLAKE_PASS@$SNOWFLAKE_ACCOUNT?warehouse=$SNOWFLAKE_WAREHOUSE"
        query: >
          select * from raw.data_integration.student_id_match_rates
          where assessment_id='{assessment_id}' and tenant_code='{tenant_code}' and school_year='{school_year}'
          order by match_rate desc
    ```