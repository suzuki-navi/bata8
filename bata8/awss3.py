
import boto3
import botocore

from bata8.lib import *

####################################################################################################

class S3Page(MenuPage):
    def canonical(self):
        return ["s3"]

    def see_also(self):
        cmd = ["bata8", "s3", "s3://.../..."]
        return [cmd]

    def items(self):
        return [("buckets", S3BucketsPage)]

    def dig(self, arg):
        if re.match("\\As3://", arg):
            return S3Page.page_from_uri(arg)
        return super().dig(arg)

    @classmethod
    def page_from_uri(cls, path):
        match = re.match("\\As3://([^/]+)\\Z", path)
        if match:
            return S3KeyPage(match.group(1), "")
        match = re.match("\\As3://([^/]+)/(.*)\\Z", path)
        if match:
            bucket_name = match.group(1)
            key = match.group(2)
            if key.endswith("/"):
                key = key[0:-1]
            try:
                return S3KeyPage(bucket_name, key)
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "AccessDenied":
                    pass
                else:
                    raise e
        return None

class S3BucketsPage(TablePage):
    def canonical(self):
        return ["s3", "buckets"]

    def nameColIdx(self):
        return 0

    def items(self):
        client = session.client("s3")
        ls = client.list_buckets()
        items = []
        for elem in ls["Buckets"]:
            items.append([elem["Name"]])
        return items

    def detailPage(self, item):
        return S3DirPage(item[0], "")

class S3BucketAltPage(MenuPage):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def items(self):
        return [
            ("versioning", S3BucketVersioningPage),
            ("policy", S3BucketPolicyPage),
        ]

    def detailPage(self, item):
        return item[1](self.bucket_name)

class S3BucketVersioningPage(ObjectPage):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def object(self):
        client = session.client("s3")
        meta = client.get_bucket_versioning(
            Bucket = self.bucket_name,
        )
        del(meta["ResponseMetadata"])
        return meta

class S3BucketPolicyPage(ObjectPage):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def object(self):
        client = session.client("s3")
        try:
            meta = client.get_bucket_policy(
                Bucket = self.bucket_name,
            )
            json_str = meta["Policy"]
            meta2 = json.loads(json_str)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchBucketPolicy":
                meta2 = None
            else:
                raise e
        return meta2

class S3KeyPage(ObjectPage):
    def __init__(self, bucket_name, key):
        self.bucket_name = bucket_name
        self.key = key
        self.info  = self._fetch_info()
        self.items = self._fetch_items()

    def _fetch_info(self):
        if self.key == "":
            return None
        try:
            client = session.client("s3")
            info = client.get_object(
                Bucket = self.bucket_name,
                Key = self.key,
            )
            del(info["ResponseMetadata"])
            del(info["Body"])
            return info
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            else:
                raise e

    def _fetch_items(self):
        client = session.client("s3")
        prefix = self._prefix()
        ls = client.list_objects_v2(
            Bucket = self.bucket_name,
            Delimiter = "/",
            Prefix = prefix,
        )
        items = []
        len_prefix = len(prefix)
        if "CommonPrefixes" in ls:
            for elem in ls["CommonPrefixes"]:
                name = elem["Prefix"]
                if name.endswith("/"):
                    name = name[0:-1]
                if name.startswith(prefix):
                    name = name[len_prefix : ]
                items.append([name, "", "", ""])
        if "Contents" in ls:
            for elem in ls["Contents"]:
                name = elem["Key"]
                if name.startswith(prefix):
                    name = name[len_prefix : ]
                items.append([name, elem["LastModified"], elem["Size"], elem["StorageClass"]])
        return items

    def _prefix(self):
        if self.key == "":
            prefix = ""
        else:
            prefix = self.key + "/"
        return prefix

    def s3path(self):
        return "s3://{}/{}".format(self.bucket_name, self.key)

    def canonical(self):
        if len(self.key) == 0:
            paths = []
        else:
            paths = self.key.split("/")
        return ["s3", "buckets", self.bucket_name] + paths

    def alt(self):
        if self.key == "":
            return S3BucketAltPage(self.bucket_name)
        return super().alt()

    def see_also(self):
        if len(self.items) == 0:
            cmd = ["aws", "s3", "cp", self.s3path(), "-"]
        else:
            cmd = ["aws", "s3", "ls", self.s3path() + "/"]
        return [cmd]

    def nameColIdx(self):
        return 0

    def object(self):
        if len(self.items) == 0:
            return self.info
        else:
            return self.items

    def detailPage(self, item):
        key = self._prefix() + item[0]
        return S3KeyPage(self.bucket_name, key)

####################################################################################################

