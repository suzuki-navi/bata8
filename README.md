# bata

自作aws cliツール

## 利用方法

dockerがインストールされていれば

    $ ./bin/bata PARAMETERS ...

dockerなしの環境で動かすには Dockerfile 参照。


## 対応しているメニュー

    cloudwatch                                                                  -> Menu
    cloudwatch events                                                           -> Menu
    cloudwatch events rules                                                     -> Table
    cloudwatch events rules <RULE_NAME>                                         -> Object
    cloudwatch logs                                                             -> Table
    cloudwatch logs <LOG_GROUP_NAME>                                            -> Table
    cloudwatch logs <LOG_GROUP_NAME> <LOG_STREAM_NAME>                          -> Table
    ecr                                                                         -> Menu
    ecr repositories                                                            -> Table
    ecr repositories <REPOSITORY_NAME>                                          -> Table
    ecr repositories <REPOSITORY_NAME> <IMAGE_ID>                               -> Object
    glue                                                                        -> Menu
    glue databases                                                              -> Table
    glue databases <DATABASE_NAME>                                              -> Table
    glue databases <DATABASE_NAME> <TABLE_NAME>                                 -> Object
    glue databases <DATABASE_NAME> --alt                                        -> Object
    glue crawlers                                                               -> Table
    glue crawlers <CRAWLER_NAME>                                                -> Object
    glue jobs                                                                   -> Table
    glue jobs <JOB_NAME>                                                        -> Menu
    glue jobs <JOB_NAME> info                                                   -> Object
    glue jobs <JOB_NAME> history                                                -> Table
    glue jobs <JOB_NAME> history <RUN_ID>                                       -> Object
    iam                                                                         -> Menu
    iam users                                                                   -> Table
    iam users <USER_NAME>                                                       -> Object
    iam roles                                                                   -> Table
    iam roles <ROLE_NAME>                                                       -> Table
    iam roles <ROLE_NAME> <POLICY_NAME>                                         -> Not implemented
    iam roles <ROLE_NAME> --alt                                                 -> Menu
    iam roles <ROLE_NAME> --alt info                                            -> Object
    iam policies                                                                -> Table
    iam policies <POLICY_NAME>                                                  -> Object
    iam policies <POLICY_NAME> --alt                                            -> Menu
    iam policies <POLICY_NAME> --alt info                                       -> Object
    iam policies <POLICY_NAME> --alt versions                                   -> Table
    iam policies <POLICY_NAME> --alt versions <VERSION_ID>                      -> Object
    lambda                                                                      -> Menu
    lambda functions                                                            -> Table
    lambda functions <FUNCTION_NAME>                                            -> Menu
    lambda functions <FUNCTION_NAME> code                                       -> Object
    lambda functions <FUNCTION_NAME> configuration                              -> Object
    lambda functions <FUNCTION_NAME> aliases                                    -> Not implemented
    rds                                                                         -> Menu
    rds databases                                                               -> Table
    rds databases <DATABASE_INSTANCE_IDENTIFIER>                                -> Not implemented
    rds databases <DATABASE_INSTANCE_IDENTIFIER> --alt                          -> Menu
    rds databases <DATABASE_INSTANCE_IDENTIFIER> --alt info                     -> Object
    s3                                                                          -> Table
    s3 buckets                                                                  -> Table
    s3 buckets <BUCKET_NAME>                                                    -> Table
    s3 buckets <BUCKET_NAME> <PREFIX> ...                                       -> Table
    s3 buckets <BUCKET_NAME> <PREFIX> ... <KEY_NAME>                            -> Not implemented
    s3 buckets <BUCKET_NAME> --alt                                              -> Menu
    s3 buckets <BUCKET_NAME> --alt versioning                                   -> Object
    s3 buckets <BUCKET_NAME> --alt policy                                       -> Object


