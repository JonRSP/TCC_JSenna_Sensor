FROM python:3.6
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD dig +short servidor | awk '{ print ; exit }' | python3 main_dummy.py 
