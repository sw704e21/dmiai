
FROM ambolt/emily:1.0.0-tf-slim

COPY requirements.txt /workspace/requirements.txt
WORKDIR /workspace

# add installation of Debian packages here

# add user with normal permission
RUN adduser --disabled-password --gecos "" emilyuser 
# add user to sudo group
RUN adduser emilyuser sudo
# set no password to sudo group
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
# set emilyuser as current user
USER emilyuser

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
