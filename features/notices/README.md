# Quick Reference
USD has a callback system that they call "Notices". These can be used to
run arbitrary commands whenever USD scene data is changed.


## Search For Stage Changes
### C++
```cpp
class UpdateNotice : public pxr::TfWeakBase
{
public:
    UpdateNotice(const pxr::UsdStageWeakPtr &stage) {
        pxr::TfNotice::Register(
            pxr::TfCreateWeakPtr(this),
            &UpdateNotice::_callback,
            stage
        );
    }

private:
    void _callback(
        const pxr::UsdNotice::ObjectsChanged &notice,
        const pxr::UsdStageWeakPtr &sender
    ) {
    }
};

int main() {
    // ... more code
    {
        UpdateNotice updated {stage};
        stage->DefinePrim(pxr::SdfPath {"/SomeSphere"});
    }
}
```


### Python
```python
# Run `update` whenever an object in `stage` changes
updated = Tf.Notice.Register(Usd.Notice.ObjectsChanged, update, stage)
stage.DefinePrim('/SomeSphere')
stage.GetPrimAtPath("/SomeSphere").SetMetadata("comment", "")

# XXX : `del` revokes the notice
del updated
stage.DefinePrim('/SomeSphere2')  # This won't trigger the `update` function
```


## Search For Global Changes
### C++
```cpp
class ObjectNoticeGlobal : public pxr::TfWeakBase
{
public:
    ObjectNoticeGlobal() {
        pxr::TfNotice::Register(
            pxr::TfCreateWeakPtr<ObjectNoticeGlobal>(this),
            &ObjectNoticeGlobal::_callback
        );
    }

private:
    void _callback(
        const pxr::UsdNotice::ObjectsChanged &notice
    ) {
        // TODO : How do you print `notice`?
        std::cout << "The triggered stage " << pxr::TfStringify(notice.GetStage()) << '\n';
    }
};


int main() {
    // ... more code

    {
        ObjectNoticeGlobal objects;
        stage->DefinePrim(pxr::SdfPath {"/Foo"});
    }
}
```


### Python
```python
objects = Tf.Notice.RegisterGlobally(Usd.Notice.ObjectsChanged, update)
stage.DefinePrim("/Foo")  # This will call `update`
```


## See Also
https://graphics.pixar.com/usd/docs/api/page_tf__notification.html

https://graphics.pixar.com/usd/docs/api/class_tf_notice.html
