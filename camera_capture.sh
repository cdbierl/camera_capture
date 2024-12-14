#!/bin/bash
trap 'kill $(jobs -p) 2>/dev/null' EXIT

app_home=/tmp/image-capture
source_name=$1
sources_cfg=$2

if [ -z ${source_name} ]; then
  echo "Please specify a source name (used for uploaded image filename.)"
  exit 1
fi

if [ -z ${sources_cfg} ]; then
  echo "Please specify a source config json file."
  exit 1
fi

if [ ! -f ${sources_cfg} ]; then
  echo "Sources config file does not exist!"
  exit 1
fi


dest_folder_id=$(jq -r .${source_name}.dest_folder_id ${sources_cfg})
if [ -z ${dest_folder_id} ]; then
  echo "Please specify destination folder id (Google Drive)"
  exit 1
fi

source_path=$(jq -r .${source_name}.path ${sources_cfg})
if [ -z ${source_path} ]; then
  echo "Please specify RTSP Url or video file"
  exit 1
fi

fps=$(jq -r .${source_name}.fps ${sources_cfg})
[ -z ${fps} ] && fps=1

img_dir=${app_home}/${source_name}
rm -rf ${img_dir}
mkdir -p ${img_dir}

extra_args=
if [ -f ${source_path} ]; then
  extra_args=" -stream_loop -1 "
fi

filepath=${img_dir}/capture.jpg

ffmpeg ${extra_args} -nostdin -rtsp_transport tcp -i ${source_path} -r ${fps} -update 1 ${filepath} &

python drive_upload.py --folder-id ${dest_folder_id} --filename ${source_name}.jpg --filepath ${filepath}

exit 0

