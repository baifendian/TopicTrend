
INSTALL_ENV=`cat ENV`
VERSION=`cat VERSION`
PRODUCT="waka_web"
PACKAGE=${PRODUCT}_${VERSION}

.PHONY: run install start reload stop 

help:
	@echo "使用前请在ENV文件输入对应的环境 <dev|tests|prod>"
	@echo "Makefile 命令列表："
	@echo "  run			以manage.py runserver方式启动"
	@echo "  install		安装服务依赖"
	@echo "  start			以uwsgi方式启动"
	@echo "  reload		重启uwsgi服务"
	@echo "  stop			停止uwsgi服务"
	@echo "  package		打包成tar.gz文件"

run:
	./manage.py runserver 0.0.0.0:8002 &

install:
	pip install -r requirements/${INSTALL_ENV}.txt

start:
	@echo "cp etc/${PRODUCT}_${INSTALL_ENV}.ini etc/${PRODUCT}.ini"
	@cp etc/${PRODUCT}_${INSTALL_ENV}.ini etc/${PRODUCT}.ini
	uwsgi --ini etc/${PRODUCT}.ini
	@echo "rm -f ../${PRODUCT}; ln -s ${PACKAGE} ../${PRODUCT}"
	
reload:
	uwsgi --reload logs/${PRODUCT}.pid;

stop:
	uwsgi --stop logs/${PRODUCT}.pid
	rm -f logs/${PRODUCT}.pid;

package:
	@echo ${PACKAGE}
	cp -R . ../${PACKAGE}
	rm -rf ../${PACKAGE}/.git
	rm -rf ../${PACKAGE}/.idea
	rm -rf ../${PACKAGE}/.settings
	find ../${PACKAGE} -name "*.pyc"  | xargs rm -f
	rm -f ../${PACKAGE}.tar.gz
	tar -zcvf ../${PACKAGE}.tar.gz ../${PACKAGE}
	rm -rf ../${PACKAGE}
