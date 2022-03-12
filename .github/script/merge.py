# coding=utf-8
# Created By Celeter
import json, shutil, datetime, os

source_type = [
    {
        'Type': '图片',
        'Value': 0
    },
    {
        'Type': '文字',
        'Value': 1
    },
    {
        'Type': '视频',
        'Value': 2
    },
    {
        'Type': '音频',
        'Value': 3
    }
]


def log(msg):
    time = datetime.datetime.now()
    print('[' + time.strftime('%Y.%m.%d %H:%M:%S') + '] ' + msg)


def read_file(f_path: str):
    with open(f_path, encoding='utf-8') as f:
        result = f.read()
    return result


def write_file(f_path: str, src):
    data = json.dumps(src, indent=2, ensure_ascii=False)
    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(data)


# 创建文件路径
def create_dir(name: str):
    if not os.path.exists(name):
        os.makedirs(name)


# 获取文件夹的路径列表
def get_folder_list(folder_dir: str):
    dir_list = os.listdir(folder_dir)
    fold_list = []
    for d in dir_list:
        sub_dir = os.path.join(folder_dir, d)
        if os.path.isdir(sub_dir):
            fold_list.append(sub_dir)
    return fold_list


# 获取文件的名称列表
def get_file_list(folder_dir: str):
    dir_list = os.listdir(folder_dir)
    f_list = []
    for d in dir_list:
        sub_dir = os.path.join(folder_dir, d)
        if os.path.isfile(sub_dir):
            f_list.append(d)
    return f_list


# 创建所有要用到的文件夹
def create_folder(import_dir: str):
    for src in source_type:
        type_dir = os.path.join(import_dir, src.get('Type'))
        create_dir(type_dir)
        create_dir(os.path.join(type_dir, '失效'))
    log('所需文件夹已生成完毕')


# 源移到对应文件夹
def sort(import_dir: str):
    f_list = get_file_list(import_dir)
    # 源分类
    for file in f_list:
        if file.endswith('.gitignore') or file.endswith('.sh') or file.endswith('.md') or file.endswith('manifest'):
            pass
        else:
            f_dir = os.path.join(import_dir, file)
            obj = json.loads(read_file(f_dir))
            for src in source_type:
                if obj.get('contentType') == src.get('Value'):
                    if file.find('失效') > -1 or not file.endswith('.json'):
                        shutil.move(f_dir, os.path.join(import_dir, src.get('Type'), '失效', file))
                    else:
                        shutil.move(f_dir, os.path.join(import_dir, src.get('Type'), file))
    log('所有源已移动到对应分类文件夹')


# 合并分类中的源
def merge(import_dir: str):
    source_list = []
    for src in source_type:
        type_dir = os.path.join(import_dir, src.get('Type'))
        f_list = get_file_list(type_dir)
        src_list = []
        for file in f_list:
            if file.endswith('.md') or file == 'sub.json':
                pass
            else:
                fileContent = read_file(os.path.join(type_dir, file)).strip()
                if fileContent.startswith("eso"):
                    src_list.append(fileContent.strip())
                    source_list.append(fileContent.strip())
                else:
                    contentJSON = json.loads(fileContent)
                    src_list.append(contentJSON)
                    source_list.append(contentJSON)
        log('{}源:{}个'.format(src.get('Type'), len(src_list)))
        write_file(os.path.join(type_dir, 'sub.json'), src_list)
        log('子分类文件{}写入完毕'.format(os.path.join(type_dir, 'sub.json')))
    log('所有源:{}个'.format(len(source_list)))
    write_file(os.path.join(import_dir, 'manifest'), source_list)
    log('所有源合并完毕，已写入文件{}'.format(os.path.join(import_dir, 'manifest')))


if __name__ == '__main__':
    # 工作路径
    # import_path = os.environ.get('GITHUB_WORKSPACE')
    import_path = "."
    if import_path is None:
        log('工作路径为空，请更改路径后再执行')
    else:
        # 创建所有要用到的文件夹
        create_folder(import_path)
        # 源分类
        # sort(import_path)
        # 源合并
        merge(import_path)
