import os

API_USER = os.getenv('ERP_API_USER') if os.getenv('ERP_API_USER') != None else 'http://172.16.152.47:8000/'

API_USER_DETAIL = API_USER + 'users/'

API_GET_INFOR='https://thongtindoanhnghiep.co/api/company/'


ENV_SETTINGS = os.getenv('ERP_ENV_SETTINGS') if os.getenv('ERP_ENV_SETTINGS') == 'production' else 'settings'

msg_tax_code_valid = 'Mã số thuế hợp lệ!'
msg_tax_code_invalid = 'Mã số thuế không hợp lệ!'
msg_tax_code_exist = 'Mã số thuế đã tồn tại!'
msg_create_success = 'Thêm mới thành công!'
msg_edit_success = 'Chỉnh sửa thành công!'
msg_delete_customer = 'Xóa thành công thông tin khách hàng: '
msg_not_permission_delete_account = 'Bạn không có quyền xóa thông tin khách hàng này!'
msg_required_name_account = 'Tên account chưa được nhập!'
msg_required_tax_code_account = 'Mã số thuế chưa được nhập!'


status_successful='successful'
status_unsuccessful='unsuccessful'
status_valid='valid'
status_invalid='invalid'
status_already_exists='already exists'
status_not_exists='doesn’t exist'
status_error='error'