#python train_disease_model.py --task_name='bpd' --batch_size=32 --epochs=10 --gpu_id='1' --do_train --lr 1e-3
#python train_disease_model.py --task_name='depression' --batch_size=32 --epochs=10 --gpu_id='1' --do_train --lr 1e-3

#python train_disease_model.py --task_name='bpd' --batch_size=32 --epochs=10 --gpu_id='1' --do_train --model_name_or_path="roberta-base" --lr 1e-3
#python train_disease_model.py --task_name='depression' --batch_size=32 --epochs=10 --gpu_id='1' --do_train --model_name_or_path="roberta-base" --lr 1e-3

#python run_disease_model.py --task_name 'bpd' --gpu_id '1' --model 'bert'
#python run_disease_model.py --task_name 'depression' --gpu_id '1' --model 'bert'
python run_disease_model.py --task_name 'bpd' --gpu_id '1' --model 'roberta'
python run_disease_model.py --task_name 'depression' --gpu_id '1' --model 'roberta'