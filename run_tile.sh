python run_infer.py \
--gpu='0,1,2,3,4,5' \
--nr_types=5 \
--type_info_path=type_info.json \
--batch_size=64 \
--model_mode=original \
--model_path=hovernet_original_consep_type_tf2pytorch.tar \
--nr_inference_workers=8 \
--nr_post_proc_workers=16 \
tile \
--input_dir=/home/liusunyan/hover_net/pre_process/tiles \
--output_dir=dataset/sample_tiles/pred/ \
--mem_usage=0.1 \
--draw_dot \
--save_qupath
