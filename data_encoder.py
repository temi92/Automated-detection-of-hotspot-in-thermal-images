import h5py

    
class DatasetWriter(object):
    def __init__(self, dims, output_path, data_key, buff_size=1000):
        self.db = h5py.File(output_path, "w")
        self.data = self.db.create_dataset(data_key, dims, dtype="float32")
        self.labels = self.db.create_dataset("labels", (dims[0],), dtype="int")
        self.buff_size = buff_size
        self.buffer = {"data":[], "labels":[]}
        self.idx = 0

        
    def meta_data(self, attr, description):
        self.data.attrs[attr] =  description
        self.labels.attrs[attr] = description

    def add_chunk(self, rows, labels):
        self.buffer["data"].extend(rows)
        self.buffer["labels"].extend(labels)
        #check to see if buffer needs to be flushed..
        if len(self.buffer["data"]) >= self.buff_size:
            #flush data...
            self.flush()


    def flush(self):
        #write to disk...
        i = self.idx + len(self.buffer["data"])
        self.data[self.idx:i]  = self.buffer["data"]
        self.labels[self.idx:i] = self.buffer["labels"]
        self.idx = i
        self.buffer = {"data":[], "labels":[]}


    def store_class_labels(self, class_labels):
        dt = h5py.special_dtype(vlen=str)

        label_set = self.db.create_dataset("label_names", (len(class_labels),),dtype=dt)
        label_set[:] = class_labels

        
    def close(self):
        if len(self.buffer["data"]) > 0:
            self.flush()

        self.db.close()

