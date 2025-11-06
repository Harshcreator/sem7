//SPDX-License-Identifier: Unlicensed
pragma solidity >=0.8.0;

contract Student {
    struct student {
        uint256 prn;
        string name;
        string class;
        string department;
    }

    uint256 private studentCount;
    mapping(uint256 => student) studentMap;

    function addStudent(
        uint256 prn,
        string memory name,
        string memory class_,
        string memory department
    ) public {
        require(prn > 0, "PRN > 0");
        require(studentMap[prn].prn == 0, "PRN exists");
        studentMap[prn] = student(prn, name, class_, department);
        studentCount += 1;
    }

    function getStudent(uint256 _id) public view returns (student memory) {
        return studentMap[_id];
    }

    function totalStudents() public view returns (uint256) {
        return studentCount;
    }

    fallback() external {
        revert("No such function");
    }
}