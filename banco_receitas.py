import csv
import os

class MiniBancoCSV:
    def __init__(self, file_path, seq_path, fields):
        self.file_path = file_path
        self.seq_path = seq_path
        self.fields = ['id'] + fields + ['deleted']  # inclui id e deleted automaticamente
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fields)
                writer.writeheader()
        # Cria arquivo .seq se não existir
        if not os.path.exists(self.seq_path):
            with open(self.seq_path, 'w', encoding='utf-8') as f:
                f.write('0')

    def _next_id(self):
        with open(self.seq_path, 'r+') as f:
            last_id = int(f.read())
            next_id = last_id + 1
            f.seek(0)
            f.write(str(next_id))
            f.truncate()
        return next_id

    def insert(self, registro: dict) -> int:
        registro = registro.copy()
        registro['id'] = self._next_id()
        registro['deleted'] = 'False'
        with open(self.file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writerow(registro)
        return registro['id']

    def get(self, filtro: dict = None, incluir_deletados=False) -> list:
        resultado = []
        with open(self.file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not incluir_deletados and row['deleted'] == 'True':
                    continue
                if filtro:
                    match = all(str(row[k]) == str(v) for k, v in filtro.items())
                    if match:
                        resultado.append(row)
                else:
                    resultado.append(row)
        return resultado

    def update(self, id: int, novos_dados: dict) -> bool:
        temp_file = self.file_path + '.tmp'
        atualizado = False
        with open(self.file_path, 'r', newline='', encoding='utf-8') as f, \
             open(temp_file, 'w', newline='', encoding='utf-8') as temp:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(temp, fieldnames=self.fields)
            writer.writeheader()
            for row in reader:
                if int(row['id']) == id:
                    for k, v in novos_dados.items():
                        if k in self.fields:
                            row[k] = v
                    atualizado = True
                writer.writerow(row)
        os.replace(temp_file, self.file_path)
        return atualizado

    def delete(self, id: int) -> bool:
        return self.update(id, {'deleted': 'True'})

    def count(self, incluir_deletados=False) -> int:
        return len(self.get(incluir_deletados=incluir_deletados))

    def vacuum(self):
        temp_file = self.file_path + '.tmp'
        with open(self.file_path, 'r', newline='', encoding='utf-8') as f, \
             open(temp_file, 'w', newline='', encoding='utf-8') as temp:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(temp, fieldnames=self.fields)
            writer.writeheader()
            for row in reader:
                if row['deleted'] != 'True':
                    writer.writerow(row)
        os.replace(temp_file, self.file_path)
