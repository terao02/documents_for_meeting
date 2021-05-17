class CLR(Callback):
    """
    kerasで使用するため、module化したCLR 
    """
    def __init__(self, step_size, base_lr, max_lr):
        super().__init__()
        self.iteration = 0
        self.step_size = step_size
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.start_lr = 0
        self.end_lr = 0
        self.history = {}
    
    def get_lr(self):
        cycle = math.floor(1 + self.iteration / (2*self.step_size))
        x = abs(self.iteration / self.step_size - 2 * cycle + 1)
        # lr = self.base_lr + (self.max_lr - self.base_lr) / cycle * max(0, (1 - x))
        lr = self.base_lr + (self.max_lr - self.base_lr) * max(0, (1 - x))
        return lr
    
    def on_train_begin(self, logs={}):
        logs = logs or {}
        
        # イテレーションごとの学習率を保存できるように追加
        self.history.setdefault("lr", [])
        
        # イテレーション数を保存するために追加
        self.history.setdefault("iterations", [])
    
    def on_batch_end(self, epoch, logs={}):
        logs = logs or {}
        self.iteration += 1
        K.set_value(self.model.optimizer.lr, self.get_lr())
    
        # 学習率を保存
        self.history["lr"].append(model.optimizer.lr.numpy())
        
        # イテレーション数を保存
        self.history["iterations"].append(self.iteration)
        
    def on_epoch_begin(self, epoch, log={}):
        self.start_lr = model.optimizer.lr.numpy()
    
    def on_epoch_end(self, epoch, log={}):
        self.end_lr = model.optimizer.lr.numpy()
        print("start lerning rate = {}, end learning rate = {} in an epoch".format(self.start_lr, self.end_lr))
