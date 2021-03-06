FROM amazonlinux

WORKDIR /
RUN yum update -y

# Install Python 3.8
RUN yum install gcc openssl-devel bzip2-devel libffi-devel wget tar gzip make -y
RUN wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz
RUN tar -xzvf Python-3.8.0.tgz
WORKDIR /Python-3.8.0
RUN ./configure --enable-optimizations
RUN make install

# Install Python 3.7
RUN yum install python3 zip -y

# Install Python packages
RUN mkdir /packages
RUN echo "imageio" >> /packages/requirements.txt
RUN echo "scipy" >> /packages/requirements.txt
RUN echo "matplotlib" >> /packages/requirements.txt

RUN mkdir -p /packages/imageio3.7/python/lib/python3.7/site-packages
RUN mkdir -p /packages/imageio3.8/python/lib/python3.8/site-packages
RUN pip3.7 install -r /packages/requirements.txt -t /packages/imageio3.7/python/lib/python3.7/site-packages
RUN pip3.8 install -r /packages/requirements.txt -t /packages/imageio3.8/python/lib/python3.8/site-packages


# Create zip files for Lambda Layer deployment
WORKDIR /packages/imageio3.7/
RUN zip -r9 /packages/imageio-python37.zip .
WORKDIR /packages/imageio3.8/
RUN zip -r9 /packages/imageio-python38.zip .
WORKDIR /packages/
RUN rm -rf /packages/imageio-python-3.7/
RUN rm -rf /packages/imageio-python-3.8/
