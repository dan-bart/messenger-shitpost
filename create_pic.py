import textwrap
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import boto3
from pic_content import sql_crawler
crawler = sql_crawler("msg_db.db")


class pic_creator():
    def __init__(self,crawler):
        self.crawler = crawler
        session = boto3.Session()
        credentials = session.get_credentials()
        self.s3 = boto3.client('s3', aws_access_key_id=credentials.access_key, 
                                     aws_secret_access_key=credentials.secret_key)

    def s3_put(self,pil_image):
        buffer = io.BytesIO()
        pil_image.save(buffer, "PNG")
        buffer.seek(0)
        self.s3.put_object(
            Body = buffer,
            Key = "final.png",
            Bucket = "fb-shitpost",
            ContentType='image/png'
        )
        
    def s3_load(self):
        obj=self.s3.get_object(
            Key = "final.png",
            Bucket = "fb-shitpost"
        )
        image = obj['Body'].read()
        dataBytesIO = io.BytesIO(image)
        return dataBytesIO

    def create_pic(self):
        self.q = self.crawler.question_content()[0]
        self.r = self.crawler.reply_content(q_name=self.q[0])[0]
        back_im = Image.open('images/background.png')
        img1 = Image.open("images/pic1.png")
        img2 = Image.open("images/pic2.png")
        img_w1, img_h1 = img1.size
        img_w2, img_h2 = img2.size
        image = back_im.copy()

        mask_img1 = Image.new("L", img1.size, 0)
        draw = ImageDraw.Draw(mask_img1)
        draw.ellipse((0, 0, img_w1, img_h1), fill=255)

        mask_img2 = Image.new("L", img2.size, 0)
        draw = ImageDraw.Draw(mask_img2)
        draw.ellipse((0, 0, img_w2, img_h2), fill=255)

        bg_w, bg_h = image.size
        offset_img1 = ((bg_w - img_w1) // 8, (bg_h - img_h1) // 8)
        offset_img2 = ((bg_w - offset_img1[0] - img_w2) // 1, (bg_h - offset_img1[1]-img_h2) // 1)
        image.paste(img1, offset_img1, mask_img1)
        image.paste(img2, offset_img2, mask_img2)

        draw = ImageDraw.Draw(image)
        font_fname ="MODERN TYPEWRITER.ttf"
        font = ImageFont.truetype(font_fname, 48)

        text_width = 40
        lines = textwrap.wrap(self.q[1], width=text_width)
        text_height = font.getsize(lines[0])[1]
        text_h_offset = offset_img1[1]+text_height
        text_w_offset = bg_w - font.getsize(lines[0])[0] - offset_img1[0]

        for line in textwrap.wrap(self.q[1], width=text_width):
            draw.text((text_w_offset, text_h_offset), line, font=font, fill="#1E1E1E")
            text_h_offset += font.getsize(line)[1]

        lines = textwrap.wrap(self.r[1], width=text_width)
        text_w_offset = offset_img1[0]
        text_h_offset =bg_h - offset_img1[1]-img_h2 + text_height

        for line in textwrap.wrap(self.r[1], width=text_width):
            draw.text((text_w_offset, text_h_offset), line, font=font, fill="#1E1E1E")
            text_h_offset += text_height
        return image
