#!/usr/bin/python3

#
# Source from https://github.com/rra94/sketchify
# 
import boto3
import botocore
import hashlib
import imageio
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.ndimage


S3_URL = "https://{bucketName}.s3.ap-northeast-2.amazonaws.com/{keyName}"
kSKETCHIFY = 'sketchify'


def dodge(front,back):

    result=front*255/(255-back) 
    result[result>255]=255
    result[back==255]=255

    return result.astype('uint8')


def grayscale(rgb):

    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


def hash_image(img_path):

    f = open(img_path,'rb')
    d = f.read()
    f.close()
    h = hashlib.sha256(d).hexdigest()

    return h

#
#  Main handler of lambda_function
#
def lambda_handler(event, context):
    #src_filename ="http://static.cricinfo.com/db/PICTURES/CMS/263600/263697.20.jpg"

    print("[DEBUG] event = {}".format(event))

    src_filename =event.get("name", None)
    h = event.get("hash", None)

    filename_set = os.path.splitext(src_filename)
    basename = filename_set[0]
    ext = filename_set[1]

    down_filename='/tmp/my_image{}'.format(ext)
    conv_filename='/tmp/sketchify{}'.format(ext)
    if os.path.exists(down_filename):
        os.remove(down_filename)
    if os.path.exists(conv_filename):
        os.remove(conv_filename)

    #
    # s3 = boto3.resource('s3')
    #
    s3 = boto3.client('s3')
    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    S3_KEY = src_filename

    try:
        # s3.Bucket(BUCKET_NAME).download_file(S3_KEY, down_filename)
        s3.download_file(BUCKET_NAME, S3_KEY, down_filename)        
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("===error message ===> {}".format(e))
            print("The object does not exist: s3://{}/{}".format(BUCKET_NAME, S3_KEY))
        else:
            raise

    #
    # Reading image to buffer.
    #
    s = imageio.imread(down_filename)
    #h = hash_image(down_filename)

    #
    # Split basename and extension from filename.
    #
    filename_set = os.path.splitext(src_filename)
    basename = filename_set[0]
    ext = filename_set[1]
    sketchify_filename='public/{}/sketchify{}'.format(h, ext)

    #
    # Grayscale.
    #
    g = grayscale(s)
    i = 255 - g

    #
    # Grayscale.
    #
    b = scipy.ndimage.filters.gaussian_filter(i, sigma=10)
    r = dodge(b, g)

    #
    # Save the converted image to a local file.
    #
    plt.imsave(conv_filename, r, cmap='gray', vmin=0, vmax=255)

    #
    # s3 = boto3.client('s3')
    #
    s3.upload_file(conv_filename, BUCKET_NAME, sketchify_filename)

    images = {
        kSKETCHIFY : S3_URL.format(bucketName = BUCKET_NAME, keyName = sketchify_filename)
    }

    return {
        "statusCode": 200,
        "body": {
            "images": images
        },
    }
