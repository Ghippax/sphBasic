#include <bits/stdc++.h>
#include "/home/libs/hdf5/include/hdf5.h"

using namespace std;

// Particle struct
struct particle{
   float x, y, z;      // Position
   float vx, vy, vz;   // Velocity
   float m;            // Mass
   float h;            // Smoothing length 
};

// Reads IC file and appends it into particle array
void readIC(vector<particle>& pArray, string path){
   // Tries to open ic file
   ifstream ic(path);
   if (!ic.is_open()) {
      cerr << "Error: Could not open file " << path << std::endl;
   }else{
      // Reads file line by line
      string line;
      while(getline(ic, line)) {
         istringstream iss(line);
         particle p;
         // Parse each column into the particle's properties
         if (!(iss >> p.x >> p.y >> p.z >> p.vx >> p.vy >> p.vz >> p.m >> p.h)) {
               cerr << "Error: Incorrect file format in line: " << line << std::endl;
               continue;
         }
         // Add particle to vector
         pArray.push_back(p); 
      }
      // Closes file when all is read
      ic.close();
   }
}

// Writes snapshot file based on the particle array
void writeSnap(vector<particle>& pArray, string path){
   // Create HDF5 file
   hid_t file_id = H5Fcreate(path.c_str(), H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);
   if (file_id < 0) {
      cerr << "Error: Unable to create file." << endl;
   }

   // Create a group named "sph"
   hid_t group_id = H5Gcreate(file_id, "sph", H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
   if (group_id < 0) {
        cerr << "Error: Unable to create group 'sph'." << endl;
        H5Fclose(file_id);
   }

   // Create and write each dataset
   const hsize_t num_particles = pArray.size();
   auto writeDataset = [&](const string& name, const float* data) {
      // Define dataspace
      hsize_t dims[1] = {num_particles}; 
      hid_t dataspace_id = H5Screate_simple(1, dims, NULL);
      if (dataspace_id < 0) {
         cerr << "Error: Unable to create dataspace for " << name << endl;
      }

      // Create dataset
      hid_t dataset_id = H5Dcreate(group_id, name.c_str(), H5T_NATIVE_FLOAT, dataspace_id,H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
      if (dataset_id < 0) {
         cerr << "Error: Unable to create dataset " << name << endl;
         H5Sclose(dataspace_id);
      }

      // Write data
      if(H5Dwrite(dataset_id, H5T_NATIVE_FLOAT, H5S_ALL, H5S_ALL, H5P_DEFAULT, data) < 0) {
         cerr << "Error: Unable to write data to dataset " << name << endl;
      }

      // Close resources
      H5Dclose(dataset_id);
      H5Sclose(dataspace_id);
   };

   // Prepare arrays for each property
   std::vector<float> x, y, z, vx, vy, vz, m, h;
   for (const auto& p : pArray) {
      x.push_back(p.x);
      y.push_back(p.y);
      z.push_back(p.z);
      vx.push_back(p.vx);
      vy.push_back(p.vy);
      vz.push_back(p.vz);
      m.push_back(p.m);
      h.push_back(p.h);
    }

   // Write datasets
   writeDataset("x", x.data());
   writeDataset("y", y.data());
   writeDataset("z", z.data());
   writeDataset("vx", vx.data());
   writeDataset("vy", vy.data());
   writeDataset("vz", vz.data());
   writeDataset("m", m.data());
   writeDataset("h", h.data());

   // Close group and file
   H5Gclose(group_id);
   H5Fclose(file_id);

   cout << "Particle data successfully written to " << path << endl;
}

// Path data
const string pathSph       = "/home/ghippax/astro/sphBasic/";
const string pathICFolder  = "IC/";
const string pathOutFolder = "out/";

const string pathIC    = "disk.dat";
const string pathSnap0 = "snap_0.hdf5";

// Main particle array
vector<particle> ps;

int main() {
   const string fullPathIC = pathSph+pathICFolder+pathIC;
   readIC(ps, fullPathIC);

   const string fullPathS0 = pathSph+pathOutFolder+pathSnap0;
   writeSnap(ps, fullPathS0);

   // Print out the particles for verification
   cout << "Read " << ps.size() << " particles." << endl;
   for (const auto& p : ps) {
      cout << "Particle: x=" << p.x << ", y=" << p.y << ", z=" << p.z
           << ", vx=" << p.vx << ", vy=" << p.vy << ", vz=" << p.vz
           << ", m=" << p.m << ", h=" << p.h << endl;
   }

   return 0;
}