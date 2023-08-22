from PIL import Image,ImageOps
import matplotlib.pyplot as plt
import ezdxf
from tqdm import tqdm
import sys

def img_to_binary(img_file, binary_file, threshold=128, is_inverted=False):
	img = Image.open(img_file)
	
	# 将图像转换为灰度图像
	gray_image = img.convert("L")

	# 对图像进行二值化处理
	binary_image = \
	gray_image.point(lambda x: 0 if x < threshold else 255, "1")	
	if is_inverted == True:
		binary_image = ImageOps.invert(binary_image)
	else:
		pass

	# 保存二值化后的图像
	binary_image.save(binary_file)
	return binary_image

def binary_to_dxf(binary_image,dxf_file):
	# 创建 DXF 文件
	doc = ezdxf.new("R2010")
	# 添加一个新的图层
	msp = doc.modelspace()
	# 获取图像的宽度和高度
	width, height = binary_image.size
	# 遍历图像的每个像素点，将黑色像素点转换为 DXF 实体
	for y in tqdm(range(height)):
	    for x in range(width):
	        # 获取像素点的颜色
	        pixel = binary_image.getpixel((x, y))
	        
	        # 如果为黑色（0），则在 DXF 文件中添加一个点实体
	        if pixel == 0:
	            msp.add_point((x, y))
	# 保存 DXF 文件
	doc.saveas(dxf_file)
	return


def plot_img(binary_image):
	plt.imshow(binary_image, cmap="gray")
	plt.title("Binary Image")
	plt.show()
	return


if __name__ == '__main__':

	try:
		img_file = sys.argv[1]
	except:
		print("ERROR: No found such an img input file!")
	try:
		binary_file = sys.argv[2]
	except:
		binary_file = "binary_img.jpg"

	# img_file, binary_file, dxf_file = "toux.jpg", "output.jpg", "output.dxf"

	try:
		dxf_file = sys.argv[3]
	except:
		dxf_file = img_file.split(".")[0]+".dxf"

	threshold=128 # 二值化阈值，默认128
	is_inverted = True # 是否反转二值化

	binary_image = img_to_binary(img_file, binary_file,threshold,is_inverted)
	binary_to_dxf(binary_image,dxf_file)
	plot_img(binary_image)

