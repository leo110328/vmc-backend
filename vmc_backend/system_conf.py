# redis配置
redis_conf_localhost = "localhost"
redis_conf_password = "Spinfo@0123"
redis_conf_port = "6379"
redis_conf_dbname = "0"
# 缓存超时事件,单位:秒
redis_conf_cache_time = 60 * 60 * 8

# mysql配置
mysql_conf_localhost = "localhost"
mysql_conf_username = "root"
mysql_conf_password = "QAZwsx123..MySql"
# mysql_conf_password = "QAZwsx123..MySql"
mysql_conf_port = "3306"
mysql_conf_dbname = "db1"

# file配置

# 文件上传后的存储路径
file_root = "/opt/data/"

# 邮件配置
email_host = 'smtp.qq.com'
email_port = 465
email_host_user = '1752476835@qq.com'
email_host_password = 'nlkxrfrsteoaddhd'

# 邮件发送标题
email_register_send_template_title = "OHRP-注冊驗証碼"
email_reset_password_send_template_title = "OHRP-重置密码驗証碼"
# 邮件发送内容， 格式为 内容***{}***内容，{}会填充验证码，形成完成的邮件内容。
# 例
# 模板 = 【这是登录的验证码，验证码{}】，验证码 = 1234
# 实际发送的邮件内容 =  【这是登录的验证码，验证码1234】
email_send_template_content = "这是登录的验证码，驗証碼内容 = {}"

# 验证码是否全部是数字
code_type_digit = True

# 启用单点登录功能
single_sign_on = True
