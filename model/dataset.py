import os, json
import torch

from torch.utils.data import Dataset, DataLoader

from transformers import AutoTokenizer

from utils import generate_examples


class DepressionDataset(Dataset):
    def __init__(self, args, mode='train', tokenizer=None):
        self.args=args
        self.label_list = [str(i) for i in range(args.num_labels)]
        self.mode = mode

        cached_features_file = os.path.join(
            args.cache_dir if args.cache_dir is not None else args.data_dir,
            "cached_{}_{}_{}_{}_{}".format(
                mode,
                tokenizer.__class__.__name__,
                str(args.max_seq_length),
                args.task_name,
                str(args.five_fold_num)
            ),
        )
        
        if os.path.exists(cached_features_file):
            print("*** Loading features from cached file {}".format(cached_features_file))
            self.features = torch.load(cached_features_file)
            self.num_data=len(self.features['labels'])

        else:
            self.data_path = args.data_path

            # train: 167,782 (15,984, 151,789) / valid: 23,968 (2,283, 21,685) / test: 47,938 (4,567, 43,371)
            with open(self.data_path.format(self.args.task_name, str(self.args.five_fold_num), self.mode), 'r') as fp:
                self.datas = json.load(fp)

            texts=[]
            labels=[]

            for idx, data in enumerate(self.datas):
                texts.append(self.datas[data][0])
                labels.append(str(self.datas[data][1]))
            assert len(texts) == len(labels), "the numbers of texts and labels are different!"
            self.num_data = len(texts)

            examples = generate_examples(mode=self.mode, texta=texts, labels=labels)


            output_mode = "classification"
            num_labels = args.num_labels
            label_map = {label: i for i, label in enumerate(self.label_list)}
            def label_from_example(label):
                if output_mode == "classification":
                    return label_map[label]
                elif output_mode == "regression":
                    return float(label)
                raise KeyError(output_mode)
            self.labels = [label_from_example(example.label) for example in examples]
            self.texts = texts


            self.encodings = tokenizer.batch_encode_plus(
                [(example.text_a, example.text_b) if example.text_b else example.text_a for example in examples],
                max_length=args.max_seq_length,
                padding='max_length',
                truncation='longest_first',
                return_tensors="pt",
            )

            self.features = self.encodings
            self.features['labels'] = torch.tensor(self.labels)
            print("*** Saving features into cached file {}".format(cached_features_file))
            torch.save(self.features, cached_features_file)


    def __len__(self):
        return len(self.features['labels'])
    

    def __getitem__(self,idx):
        item = {key: val[idx].clone().detach() for key, val in self.features.items()}
        return item

    def get_labels(self):
        return self.labels


if __name__ == '__main__':
    from train import get_args
    args = get_args()
    ds = DepressionDataset(
        args = args,
        mode='train',
        tokenizer=AutoTokenizer.from_pretrained(
            args.model_name_or_path,
            cache_dir=args.cache_dir,
        ),
    )
    dl = DataLoader(ds, batch_size=args.batch_size)
    d = next(iter(dl))
    import IPython; IPython.embed(); exit(1)
    #collections.Counter(ds.features['labels'].cpu().detach().numpy())
