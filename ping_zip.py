def zip(siteadress=None):
    import os
    import zipfile

    os.chdir('C:\GRK\logs\multiping\\')
    test_nerede = open(siteadress+".txt", "r", encoding="utf-8")
    test_dizin = test_nerede.readlines()
    test_nerede.close()
    # print(test_dizin)

    for dizin in test_dizin:
        path = r"" + str(dizin.rstrip("\n"))
        # os.chdir(path)
        # os.chdir("../")
        filePaths = []
        for root, directories, files in os.walk(path):
            for filename in files:
                filePath = os.path.join(root, filename)
                filePaths.append(filePath)
        zip_file = zipfile.ZipFile(path + '.zip', 'w', zipfile.ZIP_DEFLATED)
        with zip_file:
            for file in filePaths:
                zip_file.write(file)
        zip_file.close()