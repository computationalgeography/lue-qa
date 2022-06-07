class WorkerRange(object):

    def __init__(self, json):
        self._from_json(json)

        self.max_size = self.permutation_size(self.nr_permutations - 1)

    def _from_json(self, json):
        self.min_size = json["min_size"]
        self.max_size = json["max_size"]

        assert self.min_size > 0
        assert self.min_size <= self.max_size

    def to_json(self):
        return {
                "min_size": self.min_size,
                "max_size": self.max_size,
            }


class MultipliedWorkerRange(WorkerRange):

    def __init__(self, json):
        self.from_json(json)
        super(MultipliedWorkerRange, self).__init__(json)

    def __str__(self):
        return "MultipliedWorkerRange(min_size={}, max_size={}, multiplier={})" \
            .format(
                self.min_size,
                self.max_size,
                self.multiplier,
            )

    def from_json(self, json):
        self.multiplier = json["multiplier"]
        assert self.multiplier > 1

    def to_json(self):
        result = super(MultipliedWorkerRange, self).to_json()

        result["multiplier"] = self.multiplier

        return result

    @property
    def nr_permutations(self):
        size = self.min_size
        nr = 1

        while self.multiplier * size <= self.max_size:
            size *= self.multiplier
            nr += 1

        return nr

    def permutation_size(self,
            idx):

        assert idx in range(self.nr_permutations), idx

        size = self.min_size
        idx -= 1

        while idx >= 0:
            size *= self.multiplier
            idx -= 1

        return size


class IncrementedWorkerRange(WorkerRange):

    def __init__(self, json):
        self.from_json(json)
        super(IncrementedWorkerRange, self).__init__(json)

    def __str__(self):
        return "IncrementedWorkerRange(min_size={}, max_size={}, incrementor={})" \
            .format(
                self.min_size,
                self.max_size,
                self.incrementor,
            )

    def from_json(self, json):
        self.incrementor = json["incrementor"]
        assert self.incrementor >= 1

    def to_json(self):
        result = super(IncrementedWorkerRange, self).to_json()

        result["incrementor"] = self.incrementor

        return result

    @property
    def nr_permutations(self):
        size = self.min_size
        nr = 1

        size += self.incrementor

        while size <= self.max_size:
            size += self.incrementor
            nr += 1

        return nr

    def permutation_size(self,
            idx):

        assert idx in range(self.nr_permutations), idx

        size = self.min_size
        idx -= 1

        while idx >= 0:
            size += self.incrementor
            idx -= 1

        return size


class EmptyWorkerRange(WorkerRange):
    """
    Worker range representing a single collection of workers of a
    certain size
    """

    def __init__(self, json):
        self.from_json(json)

        super(EmptyWorkerRange, self).__init__(
            {"min_size": self.size, "max_size": self.size})
        assert self.min_size == self.max_size == self.size

    def __str__(self):
        return "EmptyWorkerRange(size={})" \
            .format(
                self.size)

    def from_json(self, json):
        self.size = json["size"]
        assert self.size >= 1

    def to_json(self):
        return {
                "size": self.size,
            }

    @property
    def nr_permutations(self):
        return 1

    def permutation_size(self,
            idx):
        assert idx == 0
        return self.size


class Pool(object):

    def __init__(self, json):
        if "multiplier" in json:
            self.range = MultipliedWorkerRange(json)
        elif "incrementor" in json:
            self.range = IncrementedWorkerRange(json)
        else:
            self.range = EmptyWorkerRange(json)

    def to_json(self):
        return self.range.to_json()

    @property
    def min_size(self):
        return self.range.min_size

    @property
    def max_size(self):
        return self.range.max_size

    @property
    def nr_permutations(self):
        return self.range.nr_permutations

    def permutation_size(self,
            idx):
        return self.range.permutation_size(idx)
