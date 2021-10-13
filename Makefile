STREAM_URL=rtsp://username:password@10.0.1.1/live
PI_IP_ADDRESS=10.0.1.1
PI_USERNAME=pi


.PHONY: run
run:
	@echo "Starting Script"
	@. env/bin/activate && export STREAM_URL=$(STREAM_URL) && cd src && python app.py

.PHONY: install
install:
	@cd scripts && bash install_pi.sh

.PHONY: copy
copy:
	@echo "For development only"
	@rsync -a $(shell pwd) --exclude env --exclude training $(PI_USERNAME)@$(PI_IP_ADDRESS):/home/$(PI_USERNAME)

.PHONY: shell
shell:
	@echo "For development only"
	@ssh $(PI_USERNAME)@$(PI_IP_ADDRESS)
 