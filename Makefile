ifneq (,$(wildcard .env))
include .env
export
endif

PACKAGE_NAME  = enigma2-plugin-extensions-madoe21-feed
VERSION       = $(shell cat VERSION | tr -d '[:space:]' | sed 's/-build$$//')

BUILD_DIR       = build
IPK_WORK_DIR    = $(BUILD_DIR)/ipk
DATA_STAGING    = $(IPK_WORK_DIR)/data
CONTROL_STAGING = $(IPK_WORK_DIR)/control

FEED_CONF_DEST = etc/opkg
OUTPUT_IPK     = $(BUILD_DIR)/$(PACKAGE_NAME)_$(VERSION)_all.ipk

DOS2UNIX_BIN := $(shell command -v dos2unix 2>/dev/null)

BOX_HOST ?=
BOX_USER ?= root
BOX_PORT ?= 22

.PHONY: all build clean prepare ipk install apply restart deploy

all: ipk

build: ipk

clean:
	rm -rf $(BUILD_DIR)

prepare:
ifneq ($(DOS2UNIX_BIN),)
	find src control -type f -exec dos2unix {} \;
endif
	mkdir -p $(DATA_STAGING)/$(FEED_CONF_DEST)
	mkdir -p $(CONTROL_STAGING)
	cp src/madoe21-feed.conf $(DATA_STAGING)/$(FEED_CONF_DEST)/
	cp control/control  $(CONTROL_STAGING)/
	cp control/postinst $(CONTROL_STAGING)/
	cp control/prerm    $(CONTROL_STAGING)/
	chmod 755 $(CONTROL_STAGING)/postinst $(CONTROL_STAGING)/prerm

ipk: clean prepare
	cd $(IPK_WORK_DIR) && \
	tar -czf data.tar.gz    -C data    . && \
	tar -czf control.tar.gz -C control . && \
	echo "2.0" > debian-binary && \
	ar r $(PACKAGE_NAME)_$(VERSION)_all.ipk debian-binary control.tar.gz data.tar.gz
	mv $(IPK_WORK_DIR)/$(PACKAGE_NAME)_$(VERSION)_all.ipk $(OUTPUT_IPK)
	@echo ""
	@echo "Built: $(OUTPUT_IPK)"

install: ipk
	@test -n "$(BOX_HOST)" || (echo "BOX_HOST not set"; exit 1)
	scp -P $(BOX_PORT) $(OUTPUT_IPK) $(BOX_USER)@$(BOX_HOST):/tmp/
	ssh -p $(BOX_PORT) $(BOX_USER)@$(BOX_HOST) \
	    "opkg install --force-reinstall /tmp/$(PACKAGE_NAME)_$(VERSION)_all.ipk && opkg update"

apply:
	@test -n "$(BOX_HOST)" || (echo "BOX_HOST not set"; exit 1)
	ssh -p $(BOX_PORT) $(BOX_USER)@$(BOX_HOST) \
	    "init 4 >/dev/null 2>&1 || killall -9 enigma2 >/dev/null 2>&1 || true; sleep 2; init 3 >/dev/null 2>&1 || true"

restart: apply

deploy: install
