# bookclub-backend


make sure to run

```
pip install requests
pip install flask
pip install flask-restful
pip install pymongo[gssapi,srv,tls]
```


first create a file named setup.xml

this contains the connection to your mongoDB server
and users for verification purposes

```xml

 <setup>
    <username>atlas username</username>
    <password>atlas password</password>
    <server>atlas db url here</server>
    <names>
        <name>Verfied User</name>
        <name>Verfied User</name>
    </names>
    <limit>int of how many books a user can post goes here</limit>
</setup>

```






