python run_infer.py \
--model_path ../pretrained/pecan-hover-net-pytorch.tar \
--gpu '0,1' \
--model_mode 'pannuke' \
--run_mode 'wsi' \
--nr_types 6 \
--nr_inference_workers 8 \
--nr_post_proc_workers 16 \
--batch_size 64 \
--ambiguous_size 128 \
--chunk_shape 10000 \
--tile_shape 2048 \
--wsi_proc_mag 40 \
--cache_path cache \
--input_dir dataset/sample_wsis/wsi/ \
--input_msk_dir dataset/sample_wsis/msk/ \
--output_dir dataset/sample_wsis/out/ \
--patch_input_shape 256 \
--patch_output_shape 164 
