install-nginx:
  pkg.installed:
  - name: nginx

nginx-running:
  service.running:
  - name: nginx
  - watch:
    - file: nginx-conf-file

nginx-conf-file:
  file.managed:
  - name: /etc/nginx/sites-enabled/default
  - source: salt://nginx-default.conf
