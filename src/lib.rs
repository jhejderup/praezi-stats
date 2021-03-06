extern crate semver;
extern crate libc;

use semver::{Version,VersionReq};
use libc::c_char;
use std::ffi::CStr;

#[no_mangle]
pub extern fn is_match(req: *const c_char, ver: *const c_char) -> bool {
    let req_str = unsafe {
        assert!(!req.is_null());
        CStr::from_ptr(req)
    };
    let ver_str = unsafe {
        assert!(!ver.is_null());
        CStr::from_ptr(ver)
    };
    
    let constraint = req_str.to_str().unwrap();
    let version = ver_str.to_str().unwrap();

    let r = match VersionReq::parse(constraint) {
        Ok(r) => r,
        Err(_) => return false,
    };

    let v = match Version::parse(version) {
        Ok(v) => v,
        Err(_) => return false,
    };

    return r.matches(&v);
}

#[no_mangle]
pub extern fn cmp(ver1: *const c_char ,ver2: *const c_char) -> i32 {
    let ver1_str = unsafe {
        assert!(!ver1.is_null());
        CStr::from_ptr(ver1)
    };
    let ver2_str = unsafe {
        assert!(!ver2.is_null());
        CStr::from_ptr(ver2)
    };

    let version1 = ver1_str.to_str().unwrap();
    let version2 = ver2_str.to_str().unwrap();

    let ver1_semver = Version::parse(version1);
    let ver2_semver = Version::parse(version2);

    if ver1_semver < ver2_semver {
        return -1;
    } else if ver1_semver > ver2_semver {
        return 1;
    } else {
        return 0;
    }
}


#[no_mangle]
pub extern fn valid(ver: *const c_char) -> bool {
    let ver_str = unsafe {
        assert!(!ver.is_null());
        CStr::from_ptr(ver)
    };
    let version = ver_str.to_str().unwrap();
    
    match Version::parse(version) {
        Ok(_) => return true,
        Err(_) => return false,
    }
}




