import pixellib
from pixellib.tune_bg import alter_bg
change_bg = alter_bg(model_type = "pb")
change_bg.load_pascalvoc_model("xception_pascalvoc.pb")
change_bg.change_bg_img(f_image_path = "images/a.jpg",b_image_path = "images/bg/bg.jfif", output_image_name="images/bg/out_put/bg.jpg")


'''
# nếu lỗi thì dùng code này
import pixellib
from pixellib.tune_bg import alter_bg

change_bg = alter_bg()
change_bg.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
change_bg.change_bg_img(f_image_path = "images/b.jfif",b_image_path = "images/bg/bg.jfif", output_image_name="images/out_put/new.jpg")
Image(filename='new_img.jpg',width=300,height=350)

'''