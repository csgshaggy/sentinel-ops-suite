import React from "react";
import { useParams } from "react-router-dom";

const AdminUserEdit: React.FC = () => {
  const { id } = useParams();
  return <div>Edit Admin User {id}</div>;
};

export default AdminUserEdit;
