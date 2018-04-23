FROM python:3

RUN mkdir -p /Wallhaven-dl/Wallhaven
WORKDIR /Wallhaven-dl

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirments.txt

COPY . .

VOLUME /Wallhaven-dl/Wallhaven

CMD [ "python", "./wallhaven-dl.py" ]
