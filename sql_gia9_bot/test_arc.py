from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

percent=0.12
if percent<0.50:
    rgb=(160,0,0)
elif 0.5<percent<0.9:
    rgb=(230,230,0)
elif percent>0.9:
    rgb=(0,160,0)
font = ImageFont.truetype(font='Times.dfont',size=140, index=0, encoding='')
img=Image.new("RGB",(640,640),(255,255,255))
draw=ImageDraw.Draw(img)
draw.ellipse((9,9,631,631),outline=(220,220,220))
draw.ellipse((71,71,569,569),outline=(220,220,220))
draw.pieslice((10,10,630,630),-90,int(360*percent)-90,fill=rgb)
draw.pieslice((70,70,570,570),-90,int(360*percent)-90,fill=(255,255,255))
draw.text((200,270), str(int(percent*100))+'%', rgb, font)
draw.ellipse((9,9,631,631),outline=(220,220,220))
draw.ellipse((71,71,569,569),outline=(220,220,220))
img.save('img/test/arc.png', 'PNG')
img.close()